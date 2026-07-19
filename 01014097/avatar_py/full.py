# import subprocess
# import os
#
# # 1. 检查 ffmpeg 路径
# ffmpeg_path = r"E:\ar\ffmpeg-7.1.1-full_build\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe"
# if not os.path.exists(ffmpeg_path):
#     raise FileNotFoundError(f"ffmpeg.exe 不存在: {ffmpeg_path}")
#
# # 2. 检查输入视频
# input_video = "video.mp4"
# if not os.path.exists(input_video):
#     raise FileNotFoundError(f"视频文件不存在: {os.path.abspath(input_video)}")
#
# # 3. 创建输出目录
# output_dir = "data/avatars/avatar_test/full_imgs"
# os.makedirs(output_dir, exist_ok=True)
# output_pattern = os.path.join(output_dir, "%08d.png")
#
# # 4. 构建命令
# command = [
#     ffmpeg_path,
#     "-i", input_video,
#     "-vf", "fps=25",
#     "-qscale:v", "2",      # 如果输出是 .jpg 可以保留；如果是 .png 可删除
#     "-y",                  # 覆盖输出
#     output_pattern
# ]
#
# # 5. 打印命令，方便调试
# print("执行命令:", " ".join(command))
#
# # 6. 执行
# try:
#     result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     print("✅ 视频帧提取成功！")
# except subprocess.CalledProcessError as e:
#     print("❌ ffmpeg 执行失败:")
#     print("错误码:", e.returncode)
#     print("错误输出:")
#     print(e.stderr)
import pandas as pd

data = pd.read_pickle('data/avatars/avatar_test/coords.pkl')


print(data)