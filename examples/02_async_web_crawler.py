"""
实战项目 2: 异步网页爬虫

一个高性能的异步网页爬虫，具有以下特性:
- 并发请求控制
- 请求限流和重试
- URL 去重
- 错误处理和日志
- 进度追踪
"""

import asyncio
import aiohttp
import time
from typing import List, Set, Dict, Optional
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass, field
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# 数据模型
# ============================================================================

@dataclass
class CrawlResult:
    """爬取结果"""
    url: str
    status: int
    success: bool
    content: Optional[str] = None
    error: Optional[str] = None
    links: List[str] = field(default_factory=list)
    elapsed: float = 0.0


@dataclass
class CrawlerStats:
    """爬虫统计"""
    total_urls: int = 0
    successful: int = 0
    failed: int = 0
    skipped: int = 0
    elapsed_time: float = 0.0
    
    @property
    def success_rate(self) -> float:
        if self.total_urls == 0:
            return 0.0
        return self.successful / self.total_urls


# ============================================================================
# 异步网页爬虫
# ============================================================================

class AsyncWebCrawler:
    """异步网页爬虫"""
    
    def __init__(
        self,
        max_concurrent: int = 10,
        max_retries: int = 3,
        timeout: float = 10.0,
        delay: float = 0.1
    ):
        """
        初始化爬虫
        
        Args:
            max_concurrent: 最大并发数
            max_retries: 最大重试次数
            timeout: 请求超时时间
            delay: 请求间隔
        """
        self.max_concurrent = max_concurrent
        self.max_retries = max_retries
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.delay = delay
        
        # 状态管理
        self.visited: Set[str] = set()
        self.results: List[CrawlResult] = []
        self.stats = CrawlerStats()
        
        # 并发控制
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.rate_limiter = asyncio.Semaphore(1)
    
    async def fetch_url(
        self,
        session: aiohttp.ClientSession,
        url: str
    ) -> CrawlResult:
        """
        获取单个 URL
        
        Args:
            session: aiohttp 会话
            url: 目标 URL
            
        Returns:
            爬取结果
        """
        start_time = time.time()
        
        async with self.semaphore:
            # 速率限制
            async with self.rate_limiter:
                await asyncio.sleep(self.delay)
            
            # 尝试多次
            for attempt in range(1, self.max_retries + 1):
                try:
                    logger.info(f"爬取 {url} (尝试 {attempt}/{self.max_retries})")
                    
                    async with session.get(
                        url,
                        timeout=self.timeout,
                        allow_redirects=True
                    ) as response:
                        content = await response.text()
                        elapsed = time.time() - start_time
                        
                        return CrawlResult(
                            url=url,
                            status=response.status,
                            success=True,
                            content=content,
                            elapsed=elapsed
                        )
                
                except asyncio.TimeoutError:
                    logger.warning(f"超时: {url} (尝试 {attempt})")
                    if attempt == self.max_retries:
                        return CrawlResult(
                            url=url,
                            status=0,
                            success=False,
                            error="超时",
                            elapsed=time.time() - start_time
                        )
                    await asyncio.sleep(1)  # 重试前等待
                
                except aiohttp.ClientError as e:
                    logger.warning(f"客户端错误: {url} - {e}")
                    return CrawlResult(
                        url=url,
                        status=0,
                        success=False,
                        error=str(e),
                        elapsed=time.time() - start_time
                    )
                
                except Exception as e:
                    logger.error(f"未知错误: {url} - {e}")
                    return CrawlResult(
                        url=url,
                        status=0,
                        success=False,
                        error=str(e),
                        elapsed=time.time() - start_time
                    )
        
        return CrawlResult(
            url=url,
            status=0,
            success=False,
            error="未知",
            elapsed=time.time() - start_time
        )
    
    async def crawl(self, urls: List[str]) -> List[CrawlResult]:
        """
        爬取多个 URL
        
        Args:
            urls: URL 列表
            
        Returns:
            爬取结果列表
        """
        start_time = time.time()
        self.stats.total_urls = len(urls)
        
        logger.info(f"开始爬取 {len(urls)} 个 URL")
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            
            for url in urls:
                if url not in self.visited:
                    self.visited.add(url)
                    task = self.fetch_url(session, url)
                    tasks.append(task)
                else:
                    self.stats.skipped += 1
            
            # 并发执行所有任务
            self.results = await asyncio.gather(*tasks, return_exceptions=False)
        
        # 统计结果
        for result in self.results:
            if result.success:
                self.stats.successful += 1
            else:
                self.stats.failed += 1
        
        self.stats.elapsed_time = time.time() - start_time
        
        logger.info(f"爬取完成: 成功 {self.stats.successful}, "
                   f"失败 {self.stats.failed}, "
                   f"跳过 {self.stats.skipped}")
        
        return self.results
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            '总URL数': self.stats.total_urls,
            '成功': self.stats.successful,
            '失败': self.stats.failed,
            '跳过': self.stats.skipped,
            '成功率': f'{self.stats.success_rate:.2%}',
            '总耗时': f'{self.stats.elapsed_time:.2f}秒',
            '平均速度': f'{self.stats.total_urls / self.stats.elapsed_time:.2f} URL/秒' 
                if self.stats.elapsed_time > 0 else 'N/A'
        }


# ============================================================================
# 递归爬虫 (爬取链接)
# ============================================================================

class RecursiveCrawler(AsyncWebCrawler):
    """递归爬虫 - 跟踪链接"""
    
    def __init__(
        self,
        max_depth: int = 2,
        same_domain_only: bool = True,
        **kwargs
    ):
        """
        初始化递归爬虫
        
        Args:
            max_depth: 最大深度
            same_domain_only: 是否只爬取同域名
        """
        super().__init__(**kwargs)
        self.max_depth = max_depth
        self.same_domain_only = same_domain_only
        self.url_queue: asyncio.Queue = asyncio.Queue()
    
    def extract_links(self, base_url: str, html: str) -> List[str]:
        """
        从 HTML 中提取链接
        
        Args:
            base_url: 基础 URL
            html: HTML 内容
            
        Returns:
            链接列表
        """
        links = []
        
        # 简单的链接提取 (实际应用应使用 BeautifulSoup)
        import re
        pattern = r'href=["\']([^"\']+)["\']'
        matches = re.findall(pattern, html)
        
        base_domain = urlparse(base_url).netloc
        
        for match in matches:
            # 转换为绝对 URL
            absolute_url = urljoin(base_url, match)
            
            # 同域名检查
            if self.same_domain_only:
                if urlparse(absolute_url).netloc != base_domain:
                    continue
            
            # 过滤掉非 http/https
            if absolute_url.startswith(('http://', 'https://')):
                links.append(absolute_url)
        
        return links
    
    async def crawl_recursive(
        self,
        start_urls: List[str]
    ) -> List[CrawlResult]:
        """
        递归爬取
        
        Args:
            start_urls: 起始 URL 列表
            
        Returns:
            所有爬取结果
        """
        # 将起始 URL 加入队列
        for url in start_urls:
            await self.url_queue.put((url, 0))  # (url, depth)
        
        async with aiohttp.ClientSession() as session:
            while not self.url_queue.empty():
                url, depth = await self.url_queue.get()
                
                # 检查深度
                if depth > self.max_depth:
                    continue
                
                # 检查是否已访问
                if url in self.visited:
                    continue
                
                self.visited.add(url)
                
                # 爬取页面
                result = await self.fetch_url(session, url)
                self.results.append(result)
                
                # 提取并加入新链接
                if result.success and result.content:
                    links = self.extract_links(url, result.content)
                    
                    for link in links[:10]:  # 限制每页链接数
                        if link not in self.visited:
                            await self.url_queue.put((link, depth + 1))
        
        return self.results


# ============================================================================
# 演示和测试
# ============================================================================

async def demo_basic_crawler():
    """演示基础爬虫"""
    print("=" * 60)
    print("基础异步爬虫演示")
    print("=" * 60)
    
    urls = [
        'https://httpbin.org/delay/1',
        'https://httpbin.org/status/200',
        'https://httpbin.org/html',
        'https://httpbin.org/json',
    ]
    
    crawler = AsyncWebCrawler(max_concurrent=2, delay=0.5)
    results = await crawler.crawl(urls)
    
    print("\n爬取结果:")
    for result in results:
        status = "✓" if result.success else "✗"
        print(f"{status} {result.url} - "
              f"状态: {result.status}, "
              f"耗时: {result.elapsed:.2f}秒")
    
    print(f"\n统计信息:")
    for key, value in crawler.get_stats().items():
        print(f"  {key}: {value}")
    print()


async def demo_error_handling():
    """演示错误处理"""
    print("=" * 60)
    print("错误处理演示")
    print("=" * 60)
    
    urls = [
        'https://httpbin.org/status/200',  # 成功
        'https://httpbin.org/status/404',  # 404
        'https://httpbin.org/status/500',  # 500
        'https://invalid-url-that-does-not-exist.com',  # 无效
    ]
    
    crawler = AsyncWebCrawler(max_concurrent=2, max_retries=2)
    results = await crawler.crawl(urls)
    
    print("\n结果:")
    for result in results:
        if result.success:
            print(f"✓ {result.url} - 状态: {result.status}")
        else:
            print(f"✗ {result.url} - 错误: {result.error}")
    print()


async def demo_rate_limiting():
    """演示速率限制"""
    print("=" * 60)
    print("速率限制演示")
    print("=" * 60)
    
    urls = [f'https://httpbin.org/delay/0.1' for _ in range(5)]
    
    # 快速爬取 (无延迟)
    print("快速爬取 (无延迟):")
    crawler_fast = AsyncWebCrawler(max_concurrent=5, delay=0)
    start = time.time()
    await crawler_fast.crawl(urls)
    fast_time = time.time() - start
    print(f"耗时: {fast_time:.2f}秒")
    
    # 限速爬取
    print("\n限速爬取 (延迟 0.5秒):")
    crawler_slow = AsyncWebCrawler(max_concurrent=5, delay=0.5)
    start = time.time()
    await crawler_slow.crawl(urls)
    slow_time = time.time() - start
    print(f"耗时: {slow_time:.2f}秒")
    print()


async def demo_progress():
    """演示进度追踪"""
    print("=" * 60)
    print("进度追踪演示")
    print("=" * 60)
    
    urls = [f'https://httpbin.org/delay/0.{i}' for i in range(10)]
    
    crawler = AsyncWebCrawler(max_concurrent=3)
    
    # 使用 asyncio.create_task 监控进度
    crawl_task = asyncio.create_task(crawler.crawl(urls))
    
    while not crawl_task.done():
        await asyncio.sleep(0.5)
        completed = len([r for r in crawler.results if r])
        print(f"进度: {completed}/{len(urls)} ({completed/len(urls)*100:.0f}%)")
    
    await crawl_task
    print(f"\n完成! 统计: {crawler.get_stats()}")
    print()


# ============================================================================
# 主程序
# ============================================================================

async def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("实战项目: 异步网页爬虫")
    print("=" * 60 + "\n")
    
    await demo_basic_crawler()
    await demo_error_handling()
    await demo_rate_limiting()
    # await demo_progress()  # 需要时间
    
    print("=" * 60)
    print("爬虫演示完成!")
    print("=" * 60)


if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())
