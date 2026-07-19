import subprocess
import os
from logger import logger

class VideoProcessor:
    """FFmpeg 视频处理器 - 简洁安全版"""

    @staticmethod
    def finalize_recording(video_path, audio_path, output_path):
        """
        合并音视频并优化输出

        Args:
            video_path: 临时视频文件路径
            audio_path: 临时音频文件路径
            output_path: 最终输出文件路径

        Returns:
            bool: 处理是否成功
        """
        try:
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # 检查输入文件是否存在
            if not os.path.exists(video_path):
                logger.error(f"视频文件不存在：{video_path}")
                return False
            if not os.path.exists(audio_path):
                logger.error(f"音频文件不存在：{audio_path}")
                return False

            # 使用双引号包裹路径，防止空格问题
            cmd = (
                f'ffmpeg -y '
                f'-i "{video_path}" '
                f'-i "{audio_path}" '
                f'-c:v copy -c:a copy '
                f'-shortest '
                f'"{output_path}"'
            )

            logger.info(f"合并音视频：{cmd}")
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60  # 超时限制
            )

            if result.returncode != 0:
                logger.error(f"FFmpeg 执行失败：{result.stderr}")
                return False

            # 清理临时文件
            try:
                os.remove(video_path)
                os.remove(audio_path)
                logger.info("临时文件已清理")
            except Exception as e:
                logger.warning(f"清理临时文件失败：{e}")

            logger.info(f"视频处理完成：{output_path}")
            return True

        except subprocess.TimeoutExpired:
            logger.error("FFmpeg 执行超时")
            return False
        except Exception as e:
            logger.error(f"视频处理异常：{str(e)}")
            return False

    @staticmethod
    def quick_compress(input_path, output_path=None):
        """
        快速压缩视频（可选功能）

        Args:
            input_path: 输入视频路径
            output_path: 输出视频路径（默认为原文件添加_compressed 后缀）

        Returns:
            str: 输出文件路径，失败返回 None
        """
        try:
            if output_path is None:
                base, ext = os.path.splitext(input_path)
                output_path = f"{base}_compressed{ext}"

            cmd = (
                f'ffmpeg -y '
                f'-i "{input_path}" '
                f'-vcodec libx264 -preset fast -crf 28 '
                f'-acodec aac -b:a 128k '
                f'"{output_path}"'
            )

            logger.info(f"压缩视频：{cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, timeout=120)

            if result.returncode == 0:
                logger.info(f"视频压缩完成：{output_path}")
                return output_path
            else:
                logger.error(f"压缩失败：{result.stderr}")
                return None

        except Exception as e:
            logger.error(f"压缩异常：{str(e)}")
            return None
