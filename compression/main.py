import zlib
import bz2
import numpy as np
import time
import sys
import io
from typing import Dict, Tuple

# 检查可选依赖是否可用
try:
    import fpzip
    FPZIP_AVAILABLE = True
except ImportError:
    FPZIP_AVAILABLE = False

try:
    import zfpy
    ZFPY_AVAILABLE = True
except ImportError:
    ZFPY_AVAILABLE = False

try:
    import h5py
    HDF5_AVAILABLE = True
except ImportError:
    HDF5_AVAILABLE = False


def compress_zlib(data: np.ndarray) -> Tuple[bytes, float]:
    """使用zlib压缩"""
    start = time.time()
    compressed = zlib.compress(data.tobytes(), level=9)
    return compressed, time.time() - start


def decompress_zlib(compressed: bytes, original_shape: tuple, dtype) -> Tuple[np.ndarray, float]:
    """使用zlib解压"""
    start = time.time()
    decompressed = np.frombuffer(zlib.decompress(
        compressed), dtype=dtype).reshape(original_shape)
    return decompressed, time.time() - start


def compress_bz2(data: np.ndarray) -> Tuple[bytes, float]:
    """使用bz2压缩"""
    start = time.time()
    compressed = bz2.compress(data.tobytes(), compresslevel=9)
    return compressed, time.time() - start


def decompress_bz2(compressed: bytes, original_shape: tuple, dtype) -> Tuple[np.ndarray, float]:
    """使用bz2解压"""
    start = time.time()
    decompressed = np.frombuffer(bz2.decompress(
        compressed), dtype=dtype).reshape(original_shape)
    return decompressed, time.time() - start


def compress_fpzip(data: np.ndarray) -> Tuple[bytes, float]:
    """使用fpzip压缩"""
    if not FPZIP_AVAILABLE:
        raise ImportError("fpzip not available")
    start = time.time()
    # fpzip.compress返回的是字节串，不需要额外处理
    compressed = fpzip.compress(data, order='C')
    return compressed, time.time() - start


def decompress_fpzip(compressed: bytes, original_shape: tuple, dtype) -> Tuple[np.ndarray, float]:
    """使用fpzip解压"""
    if not FPZIP_AVAILABLE:
        raise ImportError("fpzip not available")
    start = time.time()
    # 直接从压缩数据解压，不需要指定形状和类型
    decompressed = fpzip.decompress(compressed)
    decompressed = decompressed.squeeze()
    # 检查形状是否匹配
    if decompressed.shape != original_shape:
        raise ValueError(
            f"形状不匹配: 原始 {original_shape}, 解压后 {decompressed.shape}")
    return decompressed, time.time() - start


def compress_zfpy(data: np.ndarray) -> Tuple[bytes, float]:
    """使用zfp压缩"""
    if not ZFPY_AVAILABLE:
        raise ImportError("zfpy not available")
    start = time.time()
    compressed = zfpy.compress_numpy(data)
    return compressed, time.time() - start


def decompress_zfpy(compressed: bytes, original_shape: tuple, dtype) -> Tuple[np.ndarray, float]:
    """使用zfp解压"""
    if not ZFPY_AVAILABLE:
        raise ImportError("zfpy not available")
    start = time.time()
    decompressed = zfpy.decompress_numpy(compressed)
    return decompressed, time.time() - start


def compress_hdf5(data: np.ndarray) -> Tuple[bytes, float]:
    """使用HDF5/gzip压缩"""
    if not HDF5_AVAILABLE:
        raise ImportError("h5py not available")
    start = time.time()
    # 使用BytesIO作为内存文件
    with io.BytesIO() as f:
        with h5py.File(f, 'w') as h5f:
            h5f.create_dataset('data', data=data,
                               compression='gzip', compression_opts=9)
        compressed = f.getvalue()
    return compressed, time.time() - start


def decompress_hdf5(compressed: bytes, original_shape: tuple, dtype) -> Tuple[np.ndarray, float]:
    """使用HDF5/gzip解压"""
    if not HDF5_AVAILABLE:
        raise ImportError("h5py not available")
    start = time.time()
    with io.BytesIO(compressed) as f:
        with h5py.File(f, 'r') as h5f:
            decompressed = h5f['data'][:]
    return decompressed, time.time() - start


def compare_compression_methods(data: np.ndarray, verify: bool = True) -> Dict[str, dict]:
    """
    比较不同压缩方法的性能

    参数:
        data: 要压缩的二维numpy数组
        verify: 是否验证解压后的数据与原始数据一致

    返回:
        包含每种方法统计信息的字典
    """
    original_size = data.nbytes
    methods = {
        'zlib': (compress_zlib, decompress_zlib),
        'bz2': (compress_bz2, decompress_bz2),
    }

    if FPZIP_AVAILABLE:
        methods['fpzip'] = (compress_fpzip, decompress_fpzip)
    if ZFPY_AVAILABLE:
        methods['zfp'] = (compress_zfpy, decompress_zfpy)
    if HDF5_AVAILABLE:
        methods['hdf5_gzip'] = (compress_hdf5, decompress_hdf5)

    results = {}

    for name, (compress_fn, decompress_fn) in methods.items():
        try:
            # 压缩
            compressed_data, compress_time = compress_fn(data)
            compressed_size = len(compressed_data)

            # 解压
            decompressed_data, decompress_time = decompress_fn(
                compressed_data, data.shape, data.dtype
            )

            # 验证
            if verify:
                if not np.array_equal(data, decompressed_data):
                    max_diff = np.max(np.abs(data - decompressed_data))
                    if max_diff > 1e-6:  # 允许微小的浮点误差
                        raise ValueError(
                            f"{name} decompression failed - data mismatch (max diff: {max_diff})")

            # 计算压缩率
            compression_ratio = original_size / compressed_size

            results[name] = {
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_ratio': compression_ratio,
                'compress_time': compress_time,
                'decompress_time': decompress_time,
                # MB/s
                'throughput_compress': original_size / max(compress_time, 1e-6) / (1024**2),
                # MB/s
                'throughput_decompress': original_size / max(decompress_time, 1e-6) / (1024**2),
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
    print("\n浮点数组压缩方法比较结果:")
    print(
        f"原始数据大小: {results[next(iter(results))]['original_size']/1024:.2f} KB")
    print("-" * 80)

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
        print("-" * 60)

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
    rows, cols = 500, 500
    arr = np.random.rand(rows, cols).astype(np.float32)

    # 添加一些重复模式提高压缩率
    arr[::10, ::10] = 1.0

    print(f"测试数组大小: {rows}x{cols} ({(arr.nbytes)/1024**2:.2f} MB)")

    # 比较压缩方法
    results = compare_compression_methods(arr)

    # 打印结果
    print_comparison_results(results)
