import subprocess
import os

# 指定你的 ffmpeg 可执行文件路径
ffmpeg_path = r"E:\ar\ffmpeg-7.1.1-full_build\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe"

# 输入视频文件
input_video = "test.mp4"

# 输出图像序列的目录和命名格式
output_dir = "data/avatars/avator_test/full_imgs"  # 注意：你原文是 full_ims，但标准是 full_imgs
output_pattern = os.path.join(output_dir, "%08d.png")

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 构建 ffmpeg 命令
# 命令：ffmpeg -i test.mp4 -vf "fps=25" data/avatars/avator_test/full_imgs/frame_%04d.png
command = [
    ffmpeg_path,           # 指定 ffmpeg 可执行文件
    "-i", input_video,     # 输入文件
    "-vf", "fps=25",       # 视频滤镜：设置帧率为 25 FPS
    "-qscale:v", "2",      # （可选）设置 JPEG 质量，数值越小质量越高 (2-31)
    "-y",                  # 自动覆盖输出文件
    output_pattern         # 输出文件模式
]

# 执行命令
try:
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("视频帧提取成功！")
    print(f"图像已保存到: {output_dir}")
except subprocess.CalledProcessError as e:
    print("ffmpeg 执行失败:")
    print(e.stderr)