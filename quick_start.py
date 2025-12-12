"""
Asyncio 快速开始示例
====================
运行这个文件快速体验 asyncio 的基本功能
"""

import asyncio
import time


# ============================================================================
# 示例 1: Hello Asyncio
# ============================================================================

async def hello_asyncio():
    """最简单的异步函数"""
    print("Hello")
    await asyncio.sleep(1)
    print("Asyncio!")


# ============================================================================
# 示例 2: 并发执行对比
# ============================================================================

async def task(name, duration):
    """模拟一个需要时间的任务"""
    print(f"🚀 {name} 开始 (需要 {duration} 秒)")
    await asyncio.sleep(duration)
    print(f"✅ {name} 完成")
    return f"{name} 的结果"


async def sequential_execution():
    """顺序执行 - 慢"""
    print("\n" + "=" * 50)
    print("顺序执行（一个接一个）")
    print("=" * 50)
    
    start = time.time()
    
    result1 = await task("任务1", 2)
    result2 = await task("任务2", 2)
    result3 = await task("任务3", 2)
    
    elapsed = time.time() - start
    print(f"\n⏱️  总耗时: {elapsed:.2f} 秒")
    print(f"结果: {[result1, result2, result3]}")


async def concurrent_execution():
    """并发执行 - 快"""
    print("\n" + "=" * 50)
    print("并发执行（同时进行）")
    print("=" * 50)
    
    start = time.time()
    
    # 使用 gather 并发执行
    results = await asyncio.gather(
        task("任务1", 2),
        task("任务2", 2),
        task("任务3", 2)
    )
    
    elapsed = time.time() - start
    print(f"\n⏱️  总耗时: {elapsed:.2f} 秒")
    print(f"结果: {results}")
    print(f"\n🚀 性能提升: {6.0 / elapsed:.1f}x 更快!")


# ============================================================================
# 示例 3: 实用的并发模式
# ============================================================================

async def fetch_user(user_id):
    """模拟获取用户信息"""
    await asyncio.sleep(0.5)
    return {"id": user_id, "name": f"用户{user_id}"}


async def fetch_orders(user_id):
    """模拟获取订单信息"""
    await asyncio.sleep(0.7)
    return [{"order_id": i, "amount": 100 * i} for i in range(1, 4)]


async def fetch_user_dashboard(user_id):
    """并发获取用户仪表板数据"""
    print(f"\n📊 获取用户 {user_id} 的仪表板...")
    
    start = time.time()
    
    # 并发获取多个数据源
    user, orders = await asyncio.gather(
        fetch_user(user_id),
        fetch_orders(user_id)
    )
    
    elapsed = time.time() - start
    
    print(f"✅ 获取完成，耗时 {elapsed:.2f} 秒")
    print(f"用户: {user['name']}")
    print(f"订单数: {len(orders)}")
    print(f"如果顺序执行需要: 0.5 + 0.7 = 1.2 秒")
    
    return {"user": user, "orders": orders}


# ============================================================================
# 示例 4: 错误处理
# ============================================================================

async def task_with_error(task_id):
    """可能失败的任务"""
    await asyncio.sleep(0.5)
    
    if task_id == 2:
        raise ValueError(f"任务 {task_id} 失败了！")
    
    return f"任务 {task_id} 成功"


async def error_handling_demo():
    """演示错误处理"""
    print("\n" + "=" * 50)
    print("错误处理演示")
    print("=" * 50)
    
    # 使用 return_exceptions=True 收集所有结果
    results = await asyncio.gather(
        task_with_error(1),
        task_with_error(2),  # 这个会失败
        task_with_error(3),
        return_exceptions=True
    )
    
    # 处理结果
    for i, result in enumerate(results, 1):
        if isinstance(result, Exception):
            print(f"❌ 任务 {i}: {result}")
        else:
            print(f"✅ 任务 {i}: {result}")


# ============================================================================
# 示例 5: 超时控制
# ============================================================================

async def slow_operation():
    """慢速操作"""
    print("⏳ 开始慢速操作（需要 5 秒）...")
    await asyncio.sleep(5)
    return "完成"


async def timeout_demo():
    """超时控制演示"""
    print("\n" + "=" * 50)
    print("超时控制演示")
    print("=" * 50)
    
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=2.0)
        print(f"✅ {result}")
    except asyncio.TimeoutError:
        print("⏰ 操作超时（2秒限制）")


# ============================================================================
# 示例 6: 限制并发数量
# ============================================================================

async def api_request(semaphore, request_id):
    """模拟 API 请求"""
    async with semaphore:  # 限制并发
        print(f"  📡 请求 {request_id} 开始")
        await asyncio.sleep(1)
        print(f"  ✅ 请求 {request_id} 完成")
        return f"结果 {request_id}"


async def rate_limiting_demo():
    """并发限制演示"""
    print("\n" + "=" * 50)
    print("并发限制演示（最多 3 个并发）")
    print("=" * 50)
    
    # 创建信号量，限制最多 3 个并发
    semaphore = asyncio.Semaphore(3)
    
    start = time.time()
    
    # 创建 10 个请求，但只有 3 个会同时执行
    tasks = [api_request(semaphore, i) for i in range(1, 11)]
    results = await asyncio.gather(*tasks)
    
    elapsed = time.time() - start
    print(f"\n⏱️  完成 10 个请求，耗时 {elapsed:.2f} 秒")
    print(f"平均每个请求: {elapsed / 10:.2f} 秒")


# ============================================================================
# 主函数
# ============================================================================

async def main():
    """运行所有示例"""
    print("\n" + "=" * 70)
    print(" " * 20 + "Asyncio 快速开始")
    print("=" * 70)
    
    # 示例 1: Hello World
    print("\n【示例 1】Hello Asyncio")
    print("-" * 50)
    await hello_asyncio()
    
    # 示例 2: 顺序 vs 并发
    await sequential_execution()
    await concurrent_execution()
    
    # 示例 3: 实用模式
    print("\n" + "=" * 50)
    print("【示例 3】实用的并发模式")
    print("=" * 50)
    await fetch_user_dashboard(user_id=123)
    
    # 示例 4: 错误处理
    await error_handling_demo()
    
    # 示例 5: 超时控制
    await timeout_demo()
    
    # 示例 6: 限制并发
    await rate_limiting_demo()
    
    # 总结
    print("\n" + "=" * 70)
    print("🎉 完成！你已经掌握了 Asyncio 的基础")
    print("=" * 70)
    print("\n下一步:")
    print("  1. 阅读完整教程: asyncio_tutorial.md")
    print("  2. 学习设计模式: asyncio_design_patterns.md")
    print("  3. 运行实战示例: python practical_examples.py")
    print("  4. 查看速查表: asyncio_cheatsheet.md")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main())
