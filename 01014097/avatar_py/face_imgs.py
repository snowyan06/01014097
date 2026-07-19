#!/usr/bin/env python3
###############################################################################
#  数字人Avatar创建工具 - 从视频导入并处理生成新的数字人
#  基于LiveTalking项目结构
###############################################################################

import os
import cv2
import pickle
import numpy as np
import argparse
from tqdm import tqdm
import mediapipe as mp
import face_recognition
from pathlib import Path
import shutil


class AvatarCreator:
    def __init__(self):
        # 初始化MediaPipe人脸检测
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1, min_detection_confidence=0.7
        )

    def extract_frames_from_video(self, video_path, max_frames=200, fps_limit=None):
        """从视频中提取帧"""
        print(f"正在从视频提取帧: {video_path}")

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {video_path}")

        # 获取视频信息
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        original_fps = cap.get(cv2.CAP_PROP_FPS)

        print(f"视频总帧数: {total_frames}, 原始FPS: {original_fps}")

        frames = []
        frame_indices = []

        # 计算帧间隔
        if fps_limit:
            frame_interval = int(original_fps / fps_limit)
        else:
            frame_interval = max(1, total_frames // max_frames)

        frame_count = 0
        extracted_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_interval == 0 and extracted_count < max_frames:
                frames.append(frame)
                frame_indices.append(frame_count)
                extracted_count += 1

            frame_count += 1

        cap.release()
        print(f"提取了 {len(frames)} 帧")
        return frames, frame_indices

    def detect_and_crop_face(self, frame, padding_ratio=0.3):
        """检测人脸并裁剪"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)

        if not results.detections:
            return None, None

        # 使用第一个检测到的人脸
        detection = results.detections[0]
        bbox = detection.location_data.relative_bounding_box

        h, w = frame.shape[:2]

        # 转换为像素坐标
        x1 = int(bbox.xmin * w)
        y1 = int(bbox.ymin * h)
        x2 = int((bbox.xmin + bbox.width) * w)
        y2 = int((bbox.ymin + bbox.height) * h)

        # 添加padding
        padding_w = int((x2 - x1) * padding_ratio)
        padding_h = int((y2 - y1) * padding_ratio)

        x1 = max(0, x1 - padding_w)
        y1 = max(0, y1 - padding_h)
        x2 = min(w, x2 + padding_w)
        y2 = min(h, y2 + padding_h)

        # 裁剪人脸区域
        face_crop = frame[y1:y2, x1:x2]

        return face_crop, (y1, y2, x1, x2)

    def resize_frame(self, frame, target_size=(512, 512)):
        """调整帧大小"""
        return cv2.resize(frame, target_size, interpolation=cv2.INTER_LANCZOS4)

    def filter_stable_faces(self, frames, face_coords, similarity_threshold=0.1):
        """过滤出人脸稳定的帧"""
        print("正在过滤稳定的人脸帧...")

        if not frames:
            return [], []

        # 使用face_recognition进行人脸编码比较
        stable_frames = []
        stable_coords = []

        # 获取第一帧的人脸编码作为基准
        first_frame_rgb = cv2.cvtColor(frames[0], cv2.COLOR_BGR2RGB)
        try:
            reference_encoding = face_recognition.face_encodings(first_frame_rgb)[0]
        except IndexError:
            print("警告: 第一帧未检测到人脸编码，使用所有帧")
            return frames, face_coords

        stable_frames.append(frames[0])
        stable_coords.append(face_coords[0])

        for i, frame in enumerate(tqdm(frames[1:], desc="过滤帧")):
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            try:
                current_encodings = face_recognition.face_encodings(frame_rgb)
                if current_encodings:
                    distance = face_recognition.face_distance([reference_encoding], current_encodings[0])[0]
                    if distance < similarity_threshold:
                        stable_frames.append(frame)
                        stable_coords.append(face_coords[i + 1])
            except Exception as e:
                print(f"帧 {i + 1} 处理错误: {e}")
                continue

        print(f"从 {len(frames)} 帧中筛选出 {len(stable_frames)} 个稳定帧")
        return stable_frames, stable_coords

    def create_avatar_from_video(self, video_path, avatar_id, output_dir="./data/avatars",
                                 max_frames=200, target_size=512, fps_limit=None):
        """从视频创建avatar"""
        print(f"开始创建Avatar: {avatar_id}")

        # 创建输出目录
        avatar_path = Path(output_dir) / avatar_id
        full_imgs_path = avatar_path / "full_imgs"
        face_imgs_path = avatar_path / "face_imgs"

        # 清理并创建目录
        if avatar_path.exists():
            shutil.rmtree(avatar_path)

        avatar_path.mkdir(parents=True, exist_ok=True)
        full_imgs_path.mkdir(exist_ok=True)
        face_imgs_path.mkdir(exist_ok=True)

        # 1. 从视频提取帧
        frames, frame_indices = self.extract_frames_from_video(video_path, max_frames, fps_limit)

        # 2. 检测人脸并获取坐标
        print("正在检测人脸并裁剪...")
        valid_frames = []
        face_crops = []
        coords_list = []

        for i, frame in enumerate(tqdm(frames, desc="处理帧")):
            face_crop, coords = self.detect_and_crop_face(frame)

            if face_crop is not None and coords is not None:
                valid_frames.append(frame)
                face_crops.append(face_crop)
                coords_list.append(coords)
            else:
                print(f"警告: 帧 {i} 未检测到人脸，跳过")

        if not valid_frames:
            raise ValueError("没有检测到任何有效的人脸帧")

        print(f"检测到 {len(valid_frames)} 个有效的人脸帧")

        # 3. 过滤稳定的人脸
        stable_frames, stable_coords = self.filter_stable_faces(valid_frames, coords_list)
        stable_faces = [face_crops[valid_frames.index(frame)] for frame in stable_frames]

        # 4. 调整大小并保存
        print("正在保存处理后的图像...")

        final_coords = []

        for i, (frame, face, coords) in enumerate(zip(stable_frames, stable_faces, stable_coords)):
            # 保存完整帧 (调整到目标尺寸)
            resized_frame = self.resize_frame(frame, (target_size, target_size))
            full_img_path = full_imgs_path / f"{i:06d}.jpg"
            cv2.imwrite(str(full_img_path), resized_frame)

            # 保存人脸裁剪 (调整到目标尺寸)
            resized_face = self.resize_frame(face, (target_size, target_size))
            face_img_path = face_imgs_path / f"{i:06d}.jpg"
            cv2.imwrite(str(face_img_path), resized_face)

            # 调整坐标以适应新的图像尺寸
            original_h, original_w = frame.shape[:2]
            scale_x = target_size / original_w
            scale_y = target_size / original_h

            y1, y2, x1, x2 = coords
            scaled_coords = (
                int(y1 * scale_y),
                int(y2 * scale_y),
                int(x1 * scale_x),
                int(x2 * scale_x)
            )
            final_coords.append(scaled_coords)

        # 5. 保存坐标信息
        coords_path = avatar_path / "coords.pkl"
        with open(coords_path, 'wb') as f:
            pickle.dump(final_coords, f)

        print(f"Avatar创建完成!")
        print(f"- 总帧数: {len(final_coords)}")
        print(f"- 保存路径: {avatar_path}")
        print(f"- 图像尺寸: {target_size}x{target_size}")

        return str(avatar_path)

    def create_avatar_from_images(self, images_dir, avatar_id, output_dir="./data/avatars", target_size=512):
        """从图像文件夹创建avatar"""
        print(f"从图像文件夹创建Avatar: {avatar_id}")

        # 获取所有图像文件
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        image_files = []

        for ext in image_extensions:
            image_files.extend(Path(images_dir).glob(f"*{ext}"))
            image_files.extend(Path(images_dir).glob(f"*{ext.upper()}"))

        image_files = sorted(image_files)

        if not image_files:
            raise ValueError(f"在目录 {images_dir} 中未找到图像文件")

        print(f"找到 {len(image_files)} 个图像文件")

        # 读取所有图像
        frames = []
        for img_file in tqdm(image_files, desc="读取图像"):
            frame = cv2.imread(str(img_file))
            if frame is not None:
                frames.append(frame)
            else:
                print(f"警告: 无法读取图像 {img_file}")

        # 调用视频处理的相同逻辑
        return self._process_frames(frames, avatar_id, output_dir, target_size)

    def _process_frames(self, frames, avatar_id, output_dir, target_size):
        """处理帧的通用方法"""
        # 创建输出目录
        avatar_path = Path(output_dir) / avatar_id
        full_imgs_path = avatar_path / "full_imgs"
        face_imgs_path = avatar_path / "face_imgs"

        # 清理并创建目录
        if avatar_path.exists():
            shutil.rmtree(avatar_path)

        avatar_path.mkdir(parents=True, exist_ok=True)
        full_imgs_path.mkdir(exist_ok=True)
        face_imgs_path.mkdir(exist_ok=True)

        # 检测人脸并获取坐标
        print("正在检测人脸并裁剪...")
        valid_frames = []
        face_crops = []
        coords_list = []

        for i, frame in enumerate(tqdm(frames, desc="处理帧")):
            face_crop, coords = self.detect_and_crop_face(frame)

            if face_crop is not None and coords is not None:
                valid_frames.append(frame)
                face_crops.append(face_crop)
                coords_list.append(coords)
            else:
                print(f"警告: 帧 {i} 未检测到人脸，跳过")

        if not valid_frames:
            raise ValueError("没有检测到任何有效的人脸帧")

        # 过滤稳定的人脸
        stable_frames, stable_coords = self.filter_stable_faces(valid_frames, coords_list)
        stable_faces = [face_crops[valid_frames.index(frame)] for frame in stable_frames]

        # 保存处理后的图像
        print("正在保存处理后的图像...")
        final_coords = []

        for i, (frame, face, coords) in enumerate(zip(stable_frames, stable_faces, stable_coords)):
            # 保存完整帧
            resized_frame = self.resize_frame(frame, (target_size, target_size))
            full_img_path = full_imgs_path / f"{i:06d}.jpg"
            cv2.imwrite(str(full_img_path), resized_frame)

            # 保存人脸裁剪
            resized_face = self.resize_frame(face, (target_size, target_size))
            face_img_path = face_imgs_path / f"{i:06d}.jpg"
            cv2.imwrite(str(face_img_path), resized_face)

            # 调整坐标
            original_h, original_w = frame.shape[:2]
            scale_x = target_size / original_w
            scale_y = target_size / original_h

            y1, y2, x1, x2 = coords
            scaled_coords = (
                int(y1 * scale_y),
                int(y2 * scale_y),
                int(x1 * scale_x),
                int(x2 * scale_x)
            )
            final_coords.append(scaled_coords)

        # 保存坐标信息
        coords_path = avatar_path / "coords.pkl"
        with open(coords_path, 'wb') as f:
            pickle.dump(final_coords, f)

        print(f"Avatar创建完成!")
        print(f"- 总帧数: {len(final_coords)}")
        print(f"- 保存路径: {avatar_path}")

        return str(avatar_path)


def main():
    parser = argparse.ArgumentParser(description="数字人Avatar创建工具")
    parser.add_argument('--input', '-i', required=True, help="输入视频文件或图像文件夹路径")
    parser.add_argument('--avatar_id', '-a', required=True, help="Avatar ID (用于命名)")
    parser.add_argument('--output', '-o', default="./data/avatars", help="输出目录 (默认: ./data/avatars)")
    parser.add_argument('--max_frames', '-f', type=int, default=200, help="最大帧数 (默认: 200)")
    parser.add_argument('--target_size', '-s', type=int, default=512, help="目标图像尺寸 (默认: 512)")
    parser.add_argument('--fps_limit', type=float, default=None, help="限制提取帧率")
    parser.add_argument('--mode', '-m', choices=['video', 'images'], default='auto',
                        help="处理模式: video(视频), images(图像文件夹), auto(自动检测)")

    args = parser.parse_args()

    # 检查输入路径
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 输入路径不存在: {input_path}")
        return

    # 自动检测模式
    if args.mode == 'auto':
        if input_path.is_file():
            args.mode = 'video'
        elif input_path.is_dir():
            args.mode = 'images'
        else:
            print("错误: 无法确定输入类型")
            return

    creator = AvatarCreator()

    try:
        if args.mode == 'video':
            print(f"视频模式: {input_path}")
            creator.create_avatar_from_video(
                video_path=str(input_path),
                avatar_id=args.avatar_id,
                output_dir=args.output,
                max_frames=args.max_frames,
                target_size=args.target_size,
                fps_limit=args.fps_limit
            )
        elif args.mode == 'images':
            print(f"图像模式: {input_path}")
            creator.create_avatar_from_images(
                images_dir=str(input_path),
                avatar_id=args.avatar_id,
                output_dir=args.output,
                target_size=args.target_size
            )

        print(f"\n✅ Avatar '{args.avatar_id}' 创建成功!")
        print(f"现在您可以使用以下命令运行数字人直播:")
        print(f"python app.py --transport webrtc --model wav2lip --avatar_id {args.avatar_id}")

    except Exception as e:
        print(f"❌ 创建Avatar时出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()