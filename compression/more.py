from typing import Dict, Tuple
import sys
import io
from sklearn.decomposition import PCA
import pywt
import time
import zfpy
import numpy as np

# 检查可选依赖是否可用
try:
    import sz
    SZ_AVAILABLE = True
except ImportError:
    SZ_AVAILABLE = False

try:
    import tensorflow as tf
    import tensorflow_compression as tfc
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False


class FloatCompressor:
    """TensorFlow神经网络压缩器"""

    def __init__(self):
        self.model = self._build_model()

    def _build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Reshape((-1, 1)),
            tfc.SignalConv1D(32, (3,), corr=True, strides_down=2, padding="same_zeros",
                             use_bias=True, activation=tf.nn.relu),
            tfc.SignalConv1D(64, (3,), corr=True, strides_down=2, padding="same_zeros",
                             use_bias=True, activation=tf.nn.relu),
            tfc.SignalConv1D(128, (3,), corr=True, strides_down=2, padding="same_zeros",
                             use_bias=True, activation=None),
            tfc.NoisyDeepFactorized(bits=8),
            tfc.SignalConv1D(64, (3,), transp=True, strides_up=2, padding="same_zeros",
                             use_bias=True, activation=tf.nn.relu),
            tfc.SignalConv1D(32, (3,), transp=True, strides_up=2, padding="same_zeros",
                             use_bias=True, activation=tf.nn.relu),
            tfc.SignalConv1D(1, (3,), transp=True, strides_up=2, padding="same_zeros",
                             use_bias=True, activation=None),
            tf.keras.layers.Reshape((-1,))
        ])
        return model


def compress_zfp(data: np.ndarray, tolerance: float = 1e-3) -> Tuple[bytes, float]:
    """使用ZFP有损压缩"""
    start = time.time()
    compressed = zfpy.compress_numpy(data, tolerance=tolerance)
    return compressed, time.time() - start


def decompress_zfp(compressed: bytes) -> Tuple[np.ndarray, float]:
    """使用ZFP解压"""
    start = time.time()
    decompressed = zfpy.decompress_numpy(compressed)
    return decompressed, time.time() - start


def compress_sz(data: np.ndarray, rel_bound: float = 1e-4) -> Tuple[bytes, float]:
    """使用SZ有损压缩"""
    if not SZ_AVAILABLE:
        raise ImportError("sz not available")
    start = time.time()
    compressed = sz.compress(data, mode='REL', rel_bound=rel_bound)
    return compressed, time.time() - start


def decompress_sz(compressed: bytes) -> Tuple[np.ndarray, float]:
    """使用SZ解压"""
    if not SZ_AVAILABLE:
        raise ImportError("sz not available")
    start = time.time()
    decompressed = sz.decompress(compressed)
    return decompressed, time.time() - start


def compress_wavelet(data: np.ndarray, threshold: float = 0.1) -> Tuple[object, float]:
    """使用小波变换有损压缩"""
    start = time.time()
    coeffs = pywt.wavedec2(data, 'bior6.8', level=4)
    # 存储为字节流
    with io.BytesIO() as f:
        np.savez(f, *coeffs)
        compressed = f.getvalue()
    return compressed, time.time() - start


def decompress_wavelet(compressed: bytes) -> Tuple[np.ndarray, float]:
    """小波解压"""
    start = time.time()
    with io.BytesIO(compressed) as f:
        coeffs = list(np.load(f, allow_pickle=True).values())
    # Convert the coeffs into CORRECT type.
    for j in range(1, len(coeffs)):
        coeffs[j] = tuple(coeffs[j])
    decompressed = pywt.waverec2(coeffs, 'bior6.8')
    return decompressed, time.time() - start


def compress_pca(data: np.ndarray, variance: float = 0.95) -> Tuple[object, float]:
    """使用PCA有损压缩"""
    start = time.time()
    pca = PCA(n_components=variance)
    flattened = data.reshape(data.shape[0], -1)
    compressed = pca.fit_transform(flattened)
    # 存储为字节流
    with io.BytesIO() as f:
        np.savez(f, components=pca.components_,
                 mean=pca.mean_, compressed=compressed)
        compressed_data = f.getvalue()
    return (compressed_data, pca), time.time() - start


def decompress_pca(compressed: tuple) -> Tuple[np.ndarray, float]:
    """PCA解压"""
    compressed_data, pca = compressed
    start = time.time()
    with io.BytesIO(compressed_data) as f:
        data = np.load(f)
        decompressed = pca.inverse_transform(data['compressed'])
    # return decompressed.reshape(pca.mean_.shape), time.time() - start
    return decompressed.reshape((pca.mean_.shape[0], pca.mean_.shape[0])), time.time() - start


def compress_tf(data: np.ndarray) -> Tuple[object, float]:
    """使用TensorFlow神经网络压缩"""
    if not TF_AVAILABLE:
        raise ImportError("tensorflow_compression not available")
    start = time.time()
    compressor = FloatCompressor()
    compressed = compressor.model.predict(data[np.newaxis, ..., np.newaxis])
    return compressed, time.time() - start


def decompress_tf(compressed: np.ndarray) -> Tuple[np.ndarray, float]:
    """TensorFlow解压"""
    if not TF_AVAILABLE:
        raise ImportError("tensorflow_compression not available")
    start = time.time()
    decompressed = compressed.reshape(compressed.shape[1:-1])
    return decompressed, time.time() - start


def calculate_metrics(original: np.ndarray, decompressed: np.ndarray) -> dict:
    """计算质量指标"""
    diff = original - decompressed
    return {
        'max_error': np.max(np.abs(diff)),
        'mean_error': np.mean(np.abs(diff)),
        'psnr': 10 * np.log10(np.max(original)**2 / np.mean(diff**2)),
        'ssim': compute_ssim(original, decompressed) if original.ndim == 2 else float('nan')
    }


def compute_ssim(img1, img2):
    """计算SSIM (结构相似性)"""
    from skimage.metrics import structural_similarity
    data_range = img1.max() - img1.min()
    return structural_similarity(img1, img2, data_range=data_range)


def compare_lossy_methods(data: np.ndarray) -> Dict[str, dict]:
    """
    比较有损压缩方法

    参数:
        data: 要压缩的二维numpy数组

    返回:
        包含每种方法统计信息的字典
    """
    original_size = data.nbytes
    methods = {
        'zfp': (compress_zfp, decompress_zfp, {'tolerance': 1e-3}),
    }

    if SZ_AVAILABLE:
        methods['sz'] = (compress_sz, decompress_sz, {'rel_bound': 1e-4})

    methods['wavelet'] = (
        compress_wavelet, decompress_wavelet, {'threshold': 0.05})
    methods['pca'] = (compress_pca, decompress_pca, {'variance': 0.95})

    if TF_AVAILABLE:
        methods['tf_nn'] = (compress_tf, decompress_tf, {})

    results = {}

    for name, (compress_fn, decompress_fn, params) in methods.items():
        try:
            # 压缩
            compressed_data, compress_time = compress_fn(data, **params)
            compressed_size = sys.getsizeof(compressed_data)

            # 解压
            decompressed_data, decompress_time = decompress_fn(compressed_data)

            # 计算质量指标
            metrics = calculate_metrics(data, decompressed_data)

            # 计算压缩率
            compression_ratio = original_size / compressed_size

            results[name] = {
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_ratio': compression_ratio,
                'compress_time': compress_time,
                'decompress_time': decompress_time,
                'throughput_compress': original_size / max(compress_time, 1e-6) / (1024**2),
                'throughput_decompress': original_size / max(decompress_time, 1e-6) / (1024**2),
                'max_error': metrics['max_error'],
                'mean_error': metrics['mean_error'],
                'psnr': metrics['psnr'],
                'ssim': metrics['ssim'] if 'ssim' in metrics else float('nan'),
                'available': True,
                'error': None
            }

        except Exception as e:
            import traceback
            traceback.print_exc()
            results[name] = {
                'available': False,
                'error': str(e)
            }

    return results


def print_comparison_results(results: Dict[str, dict]):
    """打印比较结果"""
    print("\n浮点数组有损压缩方法比较结果:")
    print(
        f"原始数据大小: {results[next(iter(results))]['original_size']/1024:.2f} KB")
    print("-" * 100)

    # 按压缩率排序
    sorted_methods = sorted(
        [k for k in results if results[k]['available']],
        key=lambda x: results[x]['compression_ratio'],
        reverse=True
    )

    for method in sorted_methods:
        info = results[method]
        print(f"方法: {method.upper()}")
        print(f"  压缩后大小: {info['compressed_size']/1024:.2f} KB")
        print(f"  压缩率: {info['compression_ratio']:.2f}x")
        print(f"  压缩时间: {info['compress_time']:.4f} sec")
        print(f"  解压时间: {info['decompress_time']:.4f} sec")
        print(f"  压缩吞吐量: {info['throughput_compress']:.2f} MB/s")
        print(f"  解压吞吐量: {info['throughput_decompress']:.2f} MB/s")
        print(f"  最大误差: {info['max_error']:.2e}")
        print(f"  平均误差: {info['mean_error']:.2e}")
        print(f"  PSNR: {info['psnr']:.2f} dB")
        if not np.isnan(info['ssim']):
            print(f"  SSIM: {info['ssim']:.4f}")
        print("-" * 80)

    # 打印不可用的方法
    unavailable = [k for k in results if not results[k]['available']]
    if unavailable:
        print("\n以下方法不可用:")
        for method in unavailable:
            print(f"  {method}: {results[method]['error']}")


# 示例用法
if __name__ == "__main__":
    # 创建一个示例数组
    print("创建测试数据...")
    rows, cols = 1000, 1000
    arr = np.random.rand(rows, cols).astype(np.float32)
    arr /= np.max(arr)

    # 添加一些结构使数据可压缩
    x = np.linspace(0, 1, cols)
    y = np.linspace(0, 1, rows)
    xx, yy = np.meshgrid(x, y)
    arr = np.sin(10*xx) * np.cos(10*yy) + arr*0.1

    print(f"测试数组大小: {rows}x{cols} ({(arr.nbytes)/1024**2:.2f} MB)")

    # 比较压缩方法
    results = compare_lossy_methods(arr)

    # 打印结果
    print_comparison_results(results)
