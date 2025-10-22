"""
GlossModMCP 高级配置示例。

演示如何扩展服务器功能、添加自定义工具和优化配置。
"""

"""
================================================================================
1. 添加自定义缓存机制
================================================================================
"""

from functools import lru_cache
import time
from datetime import datetime, timedelta
from typing import Any

class CacheEntry:
    """缓存条目"""
    def __init__(self, data: Any, ttl: int = 3600):
        self.data = data
        self.created_at = datetime.now()
        self.ttl = ttl
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        return datetime.now() - self.created_at > timedelta(seconds=self.ttl)


class APICache:
    """简单的 API 缓存"""
    def __init__(self):
        self.cache: dict[str, CacheEntry] = {}
    
    def get(self, key: str) -> Any | None:
        """获取缓存"""
        if key in self.cache:
            entry = self.cache[key]
            if not entry.is_expired():
                return entry.data
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, data: Any, ttl: int = 3600):
        """设置缓存"""
        self.cache[key] = CacheEntry(data, ttl)
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()


# 使用示例
cache = APICache()

async def get_games_with_cache(page: int = 1, page_size: int = 20):
    """添加缓存的 get_games"""
    cache_key = f"games:page_{page}:size_{page_size}"
    
    # 检查缓存
    cached = cache.get(cache_key)
    if cached:
        print(f"📦 从缓存返回: {cache_key}")
        return cached
    
    # 调用原始函数
    from server import get_games
    result = await get_games(page, page_size)
    
    # 保存缓存（1小时有效期）
    cache.set(cache_key, result, ttl=3600)
    return result


"""
================================================================================
2. 错误处理和重试机制
================================================================================
"""

import httpx
from typing import TypeVar, Callable, Awaitable

T = TypeVar('T')

async def retry_on_error(
    func: Callable[..., Awaitable[T]],
    max_retries: int = 3,
    backoff_factor: float = 2.0,
    *args,
    **kwargs
) -> T:
    """
    带重试和指数退避的调用函数。
    
    参数:
    - func: 要调用的异步函数
    - max_retries: 最大重试次数
    - backoff_factor: 退避因子
    """
    last_error = None
    
    for attempt in range(max_retries):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                wait_time = (backoff_factor ** attempt)
                print(f"⚠️  重试 {attempt + 1}/{max_retries}，等待 {wait_time}s...")
                await asyncio.sleep(wait_time)
            else:
                print(f"❌ 已重试 {max_retries} 次，放弃")
    
    raise last_error or Exception("操作失败")


"""
================================================================================
3. 速率限制
================================================================================
"""

import asyncio
from collections import deque

class RateLimiter:
    """简单的速率限制器"""
    def __init__(self, calls_per_second: float = 10):
        self.calls_per_second = calls_per_second
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0.0
        self.call_times = deque()
    
    async def acquire(self):
        """获取许可"""
        now = time.time()
        
        # 移除过期的调用记录
        while self.call_times and self.call_times[0] < now - 1.0:
            self.call_times.popleft()
        
        # 检查速率限制
        if len(self.call_times) >= self.calls_per_second:
            wait_time = 1.0 - (now - self.call_times[0])
            if wait_time > 0:
                print(f"⏳ 速率限制，等待 {wait_time:.2f}s...")
                await asyncio.sleep(wait_time)
        
        self.call_times.append(time.time())


# 使用示例
rate_limiter = RateLimiter(calls_per_second=10)

async def get_games_with_ratelimit(page: int = 1):
    """带速率限制的 get_games"""
    await rate_limiter.acquire()
    from server import get_games
    return await get_games(page)


"""
================================================================================
4. 日志和监控
================================================================================
"""

import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("GlossModMCP")

class APIMetrics:
    """API 调用指标"""
    def __init__(self):
        self.total_calls = 0
        self.total_errors = 0
        self.total_cached = 0
        self.start_time = datetime.now()
    
    def record_call(self, endpoint: str, success: bool = True, from_cache: bool = False):
        """记录 API 调用"""
        self.total_calls += 1
        if not success:
            self.total_errors += 1
        if from_cache:
            self.total_cached += 1
        
        logger.info(f"API 调用: {endpoint}, 成功: {success}, 缓存: {from_cache}")
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        duration = (datetime.now() - self.start_time).total_seconds()
        return {
            "总调用数": self.total_calls,
            "错误数": self.total_errors,
            "缓存命中": self.total_cached,
            "运行时间(秒)": duration,
            "成功率": (1 - self.total_errors / max(1, self.total_calls)) * 100,
            "吞吐量(调用/秒)": self.total_calls / max(1, duration),
        }


metrics = APIMetrics()


"""
================================================================================
5. 批量操作助手
================================================================================
"""

async def batch_get_game_details(game_ids: list[int]) -> dict:
    """
    批量获取多个游戏的详细信息。
    
    演示如何使用并发操作优化性能。
    """
    from server import get_game_detail
    import concurrent.futures
    
    # 限制并发数
    semaphore = asyncio.Semaphore(5)
    
    async def fetch_with_limit(game_id: int):
        async with semaphore:
            try:
                result = await get_game_detail(game_id)
                metrics.record_call(f"get_game_detail/{game_id}", success=True)
                return game_id, result
            except Exception as e:
                metrics.record_call(f"get_game_detail/{game_id}", success=False)
                logger.error(f"获取游戏 {game_id} 失败: {e}")
                return game_id, None
    
    # 并发调用
    tasks = [fetch_with_limit(gid) for gid in game_ids]
    results = await asyncio.gather(*tasks)
    
    return {
        gid: result for gid, result in results if result is not None
    }


"""
================================================================================
6. 数据转换和格式化
================================================================================
"""

class GameFormatter:
    """游戏数据格式化器"""
    
    @staticmethod
    def to_markdown(game: dict) -> str:
        """将游戏数据转换为 Markdown"""
        return f"""
# {game.get('name', 'N/A')}

- **ID**: {game.get('id', 'N/A')}
- **英文名**: {game.get('englishName', 'N/A')}
- **总 Mod 数**: {game.get('allcount', 'N/A')}
- **最近30天 Mod 数**: {game.get('tcount', 'N/A')}

## 描述

{game.get('description', 'N/A')}
"""
    
    @staticmethod
    def to_json(game: dict) -> dict:
        """转换为 JSON 格式"""
        return {
            "id": game.get('id'),
            "name": game.get('name'),
            "englishName": game.get('englishName'),
            "modCount": game.get('allcount'),
            "recentModCount": game.get('tcount'),
            "description": game.get('description'),
        }
    
    @staticmethod
    def to_csv_row(game: dict) -> str:
        """转换为 CSV 行"""
        return f"{game.get('id')},{game.get('name')},{game.get('englishName')},{game.get('allcount')}"


"""
================================================================================
7. 使用示例
================================================================================
"""

async def main():
    """演示高级功能"""
    print("🚀 GlossModMCP 高级功能演示\n")
    
    # 演示 1: 缓存
    print("1️⃣  缓存演示")
    print("-" * 50)
    result1 = await get_games_with_cache(page=1)
    print(f"✓ 第一次调用完成")
    result2 = await get_games_with_cache(page=1)
    print(f"✓ 第二次调用从缓存返回\n")
    
    # 演示 2: 指标
    print("2️⃣  API 指标演示")
    print("-" * 50)
    stats = metrics.get_stats()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")
    print()
    
    # 演示 3: 速率限制
    print("3️⃣  速率限制演示")
    print("-" * 50)
    print("此演示将进行快速连续调用，演示速率限制效果")
    print("(为了节省时间，这里仅显示说明)\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
