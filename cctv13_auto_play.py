"""
CCTV13 自动播放脚本 - 24 小时持续播放监控（强制全屏版）
功能：
1. 浏览器窗口最大化（1920x1080）
2. 使用 JS 强制全屏（不再依赖 F11）
3. 每 600 秒自动刷新页面
4. 每 30 秒检测视频播放状态

核心修改：
- 直接使用 JS requestFullscreen
- 不依赖 F11 快捷键
- 强制全屏容器
"""

import asyncio
import logging
from playwright.async_api import async_playwright
import sys
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('cctv13_auto_play.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

CCTV13_URL = "https://tv.cctv.com/live/cctv13/"
CHECK_INTERVAL = 30  # 检测间隔（秒）
REFRESH_INTERVAL = 600  # 刷新间隔（秒，10 分钟）

class CCTV13AutoPlayer:
    """CCTV13 自动播放控制器"""
    
    def __init__(self):
        self.browser = None
        self.page = None
        self.context = None
        self.running = True
        self.check_count = 0
        self.recover_count = 0
        self.refresh_count = 0
        
    async def setup_browser(self):
        """启动浏览器并设置窗口大小"""
        try:
            logger.info("正在启动浏览器...")
            
            # 启动浏览器
            self.browser = await self.playwright.chromium.launch(
                headless=False,
                args=[
                    "--disable-gpu",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                ]
            )
            
            # 使用 1920x1080 作为视口
            screen_width = 1920
            screen_height = 1080
            
            logger.info(f"设置视口尺寸：{screen_width}x{screen_height}")
            
            # 创建浏览器上下文 - 使用屏幕尺寸
            self.context = await self.browser.new_context(
                viewport={"width": screen_width, "height": screen_height}
            )
            
            # 创建页面
            self.page = await self.context.new_page()
            
            await asyncio.sleep(1)
            
            # 设置页面视口为屏幕尺寸
            await self.page.set_viewport_size({"width": screen_width, "height": screen_height})
            
            # 等待浏览器启动完成
            await asyncio.sleep(2)
            
            logger.info(f"✅ 浏览器已启动，视口：{screen_width}x{screen_height}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 浏览器启动失败：{e}")
            return False
    
    async def load_page(self):
        """加载 CCTV13 页面"""
        try:
            logger.info(f"正在加载：{CCTV13_URL}")
            await self.page.goto(CCTV13_URL, wait_until="networkidle", timeout=60000)
            
            # 等待视频元素加载
            await self.page.wait_for_selector("video", timeout=30000)
            
            # 等待 3 秒确保视频缓冲
            await asyncio.sleep(4)
            
            # 第一步：强制全屏
            logger.info("正在强制全屏...")
            await self.force_fullscreen()
            
            # 等待 2 秒确保全屏生效
            await asyncio.sleep(2)
            
            # 检查是否全屏成功
            is_fullscreen = await self.check_fullscreen()
            logger.info(f"✅ CCTV13 页面加载完成，当前全屏状态：{'是' if is_fullscreen else '否'}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 页面加载失败：{e}")
            return False
    
    async def force_fullscreen(self):
        """强制全屏 - 使用 JavaScript 调用 requestFullscreen"""
        try:
            # 方法 1：视频全屏
            result = await self.page.evaluate("""
                () => {
                    var results = [];
                    
                    // 尝试视频全屏
                    var video = document.querySelector('video');
                    if (video) {
                        try {
                            if (video.requestFullscreen) {
                                video.requestFullscreen();
                                results.push({type: 'video', method: 'fullscreen', success: true});
                            } else if (video.webkitRequestFullscreen) {
                                video.webkitRequestFullscreen();
                                results.push({type: 'video', method: 'webkit', success: true});
                            } else if (video.mozRequestFullScreen) {
                                video.mozRequestFullScreen();
                                results.push({type: 'video', method: 'moz', success: true});
                            }
                        } catch (e) {
                            results.push({type: 'video', success: false, error: e.message});
                        }
                    }
                    
                    // 尝试 container 全屏
                    var container = document.querySelector('.video-player, .player, .alivp-container, .aliplayer');
                    if (container) {
                        try {
                            if (container.requestFullscreen) {
                                container.requestFullscreen();
                                results.push({type: 'container', method: 'fullscreen', success: true});
                            }
                        } catch (e) {
                            results.push({type: 'container', success: false, error: e.message});
                        }
                    }
                    
                    // 尝试 document.body 全屏
                    try {
                        if (document.body.requestFullscreen) {
                            document.body.requestFullscreen();
                            results.push({type: 'body', method: 'fullscreen', success: true});
                        }
                    } catch (e) {
                        results.push({type: 'body', success: false, error: e.message});
                    }
                    
                    // 尝试 document.documentElement 全屏
                    try {
                        if (document.documentElement.requestFullscreen) {
                            document.documentElement.requestFullscreen();
                            results.push({type: 'document', method: 'fullscreen', success: true});
                        }
                    } catch (e) {
                        results.push({type: 'document', success: false, error: e.message});
                    }
                    
                    return results;
                }
            """)
            
            logger.info(f"✅ JS 全屏执行完成，结果：{len(result)} 种方法已尝试")
            for r in result:
                if r.get('success'):
                    logger.info(f"  - {r['type']} 全屏：{r['method']} ✅")
                else:
                    logger.info(f"  - {r['type']} 全屏：失败 ({r.get('error')})")
            
            return True
        except Exception as e:
            logger.error(f"❌ 强制全屏失败：{e}")
            return False
    
    async def check_fullscreen(self):
        """检查浏览器是否全屏"""
        try:
            is_fullscreen = await self.page.evaluate("""
                () => {
                    // 检查任何元素是否全屏
                    var fullscreenElement = document.fullscreenElement || 
                                             document.webkitFullscreenElement || 
                                             document.mozFullScreenElement || 
                                             document.msFullscreenElement;
                    return fullscreenElement !== null;
                }
            """)
            return is_fullscreen
        except Exception as e:
            logger.error(f"检查全屏状态失败：{e}")
            return False
    
    async def check_video_status(self):
        """检查视频播放状态"""
        try:
            video_status = await self.page.evaluate("""
                () => {
                    var video = document.querySelector('video');
                    if (!video) {
                        return {found: false, playing: false, paused: true};
                    }
                    return {
                        found: true,
                        playing: !video.paused && !video.ended,
                        paused: video.paused,
                        ended: video.ended
                    };
                }
            """)
            return video_status
        except Exception as e:
            logger.error(f"❌ 检查视频状态失败：{e}")
            return None
    
    async def click_play(self):
        """恢复播放"""
        try:
            result = await self.page.evaluate("""
                () => {
                    var video = document.querySelector('video');
                    if (video) {
                        try {
                            video.play();
                            return {success: true};
                        } catch (e) {
                            return {success: false, message: e.message};
                        }
                    }
                    return {success: false, message: 'No video'};
                }
            """)
            
            if result.get('success'):
                logger.info("✅ 已通过 JS 恢复播放")
                return True
            else:
                logger.warning(f"⚠️ JS 播放失败：{result.get('message')}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 播放恢复失败：{e}")
            return False
    
    async def refresh_and_fullscreen(self):
        """刷新页面并全屏"""
        try:
            logger.warning("⚠️ 准备刷新页面...")
            await self.page.reload(wait_until="networkidle")
            
            # 等待视频加载
            await self.page.wait_for_selector("video", timeout=30000)
            await asyncio.sleep(3)
            
            logger.warning("⏳ 刷新完成，正在强制全屏...")
            await self.force_fullscreen()
            
            logger.info("✅ 页面已刷新并全屏")
            self.refresh_count += 1
            return True
            
        except Exception as e:
            logger.error(f"❌ 刷新页面失败：{e}")
            return False
    
    async def monitor(self):
        """主监控循环"""
        logger.info(f"开始监控，每{CHECK_INTERVAL}秒检测一次...")
        logger.info(f"每{REFRESH_INTERVAL}秒自动刷新页面（{REFRESH_INTERVAL/60}分钟）...")
        logger.info("按 Ctrl+C 停止程序")
        
        last_refresh_time = 0
        
        while self.running:
            try:
                await asyncio.sleep(CHECK_INTERVAL)
                self.check_count += 1
                
                # 计算时间间隔
                current_time = self.check_count * CHECK_INTERVAL
                time_since_refresh = current_time - last_refresh_time
                
                # 检查是否需要刷新（每 600 秒）
                should_refresh = time_since_refresh >= REFRESH_INTERVAL
                
                # 检查视频状态
                video_status = await self.check_video_status()
                
                if not video_status:
                    logger.error("❌ 无法获取视频状态，尝试刷新...")
                    should_refresh = True
                elif not video_status['found']:
                    logger.error("❌ 未找到视频元素，尝试刷新...")
                    should_refresh = True
                
                # 决定是否刷新
                if should_refresh:
                    await self.refresh_and_fullscreen()
                    last_refresh_time = current_time
                    
                    # 刷新后重新检查
                    video_status = await self.check_video_status()
                
                # 检查全屏状态
                is_fullscreen = await self.check_fullscreen()
                
                # 记录状态
                if video_status:
                    is_playing = video_status['playing']
                    is_paused = video_status['paused']
                    
                    # 记录日志
                    status_str = f"全屏={'是'if is_fullscreen else '否'}, 播放={'是'if is_playing else '否'}"
                    logger.info(f"状态检查：{status_str}")
                    
                    # 检查结果
                    if is_playing and is_fullscreen:
                        logger.info(f"[检查 #{self.check_count}] ✅ 视频全屏播放中")
                    elif is_playing and not is_fullscreen:
                        logger.warning(f"[检查 #{self.check_count}] ⚠️ 视频播放中但未全屏")
                    elif not is_playing and is_paused:
                        logger.warning(f"[检查 #{self.check_count}] ⚠️ 视频已暂停")
                        
                        # 恢复播放
                        await self.click_play()
                        self.recover_count += 1
                    else:
                        logger.info(f"[检查 #{self.check_count}] 状态正常")
                    
                    # 每刷新一次记录
                    if should_refresh:
                        logger.info(f"[刷新 #{self.refresh_count}] 页面已刷新，运行时间：{current_time/60:.1f}分钟")
                
            except KeyboardInterrupt:
                logger.info("收到停止指令")
                break
            except Exception as e:
                logger.error(f"监控异常：{e}")
                try:
                    await asyncio.sleep(10)
                except:
                    pass
    
    async def cleanup(self):
        """清理资源"""
        logger.info("正在关闭程序...")
        self.running = False
        
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
            
        logger.info("=" * 50)
        logger.info("程序运行统计:")
        logger.info(f"检测次数：{self.check_count}")
        logger.info(f"恢复次数：{self.recover_count}")
        logger.info(f"刷新次数：{self.refresh_count}")
        logger.info(f"运行时间：{self.check_count * CHECK_INTERVAL / 60:.1f} 分钟")
        logger.info("=" * 50)
    
    async def run(self):
        """主入口"""
        async with async_playwright() as p:
            self.playwright = p
            
            try:
                if not await self.setup_browser():
                    return False
                if not await self.load_page():
                    return False
                await self.monitor()
                
            except KeyboardInterrupt:
                pass
            finally:
                await self.cleanup()


if __name__ == "__main__":
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW("CCTV13 自动播放监控 - 强制全屏版")
    except:
        pass
    
    print("\n" + "=" * 50)
    print("CCTV13 自动播放监控脚本 - 强制全屏版")
    print("核心改进：")
    print("  ✅ 不依赖 F11 快捷键")
    print("  ✅ 直接使用 JS requestFullscreen")
    print("  ✅ 多方法尝试：video/container/body/document")
    print("  ✅ 每 10 分钟自动刷新 + 全屏")
    print("  ✅ 每 30 秒检测全屏 + 播放状态")
    print("功能：")
    print("  - 自动启动浏览器并最大化窗口")
    print("  - 自动加载 CCTV13 直播")
    print("  - 强制 JS 全屏（多种方法）")
    print("  - 每 600 秒自动刷新并全屏")
    print("  - 暂停自动恢复播放")
    print("  - 24 小时持续监控")
    print("提示：")
    print("  - 放弃 F11，使用 JS 强制全屏")
    print("  - 如果全屏无效，可能是播放器拦截")
    print("  - 按 Ctrl+C 停止程序")
    print("=" * 50 + "\n")
    
    player = CCTV13AutoPlayer()
    asyncio.run(player.run())
