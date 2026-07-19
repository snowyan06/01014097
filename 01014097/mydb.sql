/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3307
 Source Server Type    : MySQL
 Source Server Version : 50738 (5.7.38)
 Source Host           : localhost:3307
 Source Schema         : mydb

 Target Server Type    : MySQL
 Target Server Version : 50738 (5.7.38)
 File Encoding         : 65001

 Date: 22/07/2025 12:31:19
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for knowledge_dependencies
-- ----------------------------
DROP TABLE IF EXISTS `knowledge_dependencies`;
CREATE TABLE `knowledge_dependencies`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `parent` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `child` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '关联的用户ID（UUID）',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `parent`(`parent`, `user_id`) USING BTREE,
  INDEX `child`(`child`, `user_id`) USING BTREE,
  CONSTRAINT `knowledge_dependencies_ibfk_1` FOREIGN KEY (`parent`, `user_id`) REFERENCES `knowledge_points` (`name`, `user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `knowledge_dependencies_ibfk_2` FOREIGN KEY (`child`, `user_id`) REFERENCES `knowledge_points` (`name`, `user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 127 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of knowledge_dependencies
-- ----------------------------
INSERT INTO `knowledge_dependencies` VALUES (75, '嵌入式系统', '定义', '7');
INSERT INTO `knowledge_dependencies` VALUES (76, '嵌入式系统', '嵌入式Linux开发工具', '7');
INSERT INTO `knowledge_dependencies` VALUES (77, 'Linux系统', '内核配置', '7');
INSERT INTO `knowledge_dependencies` VALUES (78, '嵌入式Linux开发工具', '内核配置', '7');
INSERT INTO `knowledge_dependencies` VALUES (79, '内核编译', '硬件架构', '7');
INSERT INTO `knowledge_dependencies` VALUES (80, '内核编译', '操作系统移植', '7');
INSERT INTO `knowledge_dependencies` VALUES (81, '操作系统移植', '硬件兼容性', '7');
INSERT INTO `knowledge_dependencies` VALUES (82, '烧录过程', '硬件兼容性', '7');
INSERT INTO `knowledge_dependencies` VALUES (83, '外设与接口', 'SPI总线', '7');
INSERT INTO `knowledge_dependencies` VALUES (84, 'SPI总线', '全双工通信方式', '7');
INSERT INTO `knowledge_dependencies` VALUES (85, 'I2C总线', '串行通信', '7');
INSERT INTO `knowledge_dependencies` VALUES (86, 'I2C总线', '同步通信', '7');
INSERT INTO `knowledge_dependencies` VALUES (87, 'I2C总线', '主从通信', '7');
INSERT INTO `knowledge_dependencies` VALUES (88, '通信类型', '串行通信', '7');
INSERT INTO `knowledge_dependencies` VALUES (89, '通信类型', '同步通信', '7');
INSERT INTO `knowledge_dependencies` VALUES (90, '通信类型', '主从通信', '7');
INSERT INTO `knowledge_dependencies` VALUES (91, '嵌入式系统', 'SPI总线', '7');
INSERT INTO `knowledge_dependencies` VALUES (92, 'SPI总线', '通信协议', '7');
INSERT INTO `knowledge_dependencies` VALUES (93, 'SPI总线', '数据线', '7');
INSERT INTO `knowledge_dependencies` VALUES (94, 'USB接口', '设备连接类型', '7');
INSERT INTO `knowledge_dependencies` VALUES (95, 'USB接口', '外设支持', '7');
INSERT INTO `knowledge_dependencies` VALUES (96, '嵌入式系统定义', '计算机系统基础', '7');
INSERT INTO `knowledge_dependencies` VALUES (97, '嵌入式系统定义', '专用系统功能', '7');
INSERT INTO `knowledge_dependencies` VALUES (98, '嵌入式系统定义', '实时性要求', '7');
INSERT INTO `knowledge_dependencies` VALUES (99, '嵌入式系统定义', '硬件与软件集成', '7');
INSERT INTO `knowledge_dependencies` VALUES (100, '专用系统功能', '嵌入式系统定义', '7');
INSERT INTO `knowledge_dependencies` VALUES (101, '实时性要求', '嵌入式系统定义', '7');
INSERT INTO `knowledge_dependencies` VALUES (102, '硬件与软件集成', '嵌入式系统定义', '7');
INSERT INTO `knowledge_dependencies` VALUES (104, '嵌入式系统', 'Linux系统', '7');
INSERT INTO `knowledge_dependencies` VALUES (105, 'Linux系统', '内核配置', '7');
INSERT INTO `knowledge_dependencies` VALUES (106, '内核配置', '内核功能工具', '7');
INSERT INTO `knowledge_dependencies` VALUES (107, 'Linux内核驱动开发', '字符设备注册', '7');
INSERT INTO `knowledge_dependencies` VALUES (108, '字符设备注册', 'register_chrdev_region 函数', '7');
INSERT INTO `knowledge_dependencies` VALUES (109, '字符设备注册', '设备号分配', '7');
INSERT INTO `knowledge_dependencies` VALUES (110, 'RTOS', '实时操作系统', '7');
INSERT INTO `knowledge_dependencies` VALUES (111, '实时操作系统', '核心机制', '7');
INSERT INTO `knowledge_dependencies` VALUES (112, '接口类型', '传感器', '5');
INSERT INTO `knowledge_dependencies` VALUES (113, '接口类型', '微控制器', '5');
INSERT INTO `knowledge_dependencies` VALUES (114, '嵌入式系统', '定义', '7');
INSERT INTO `knowledge_dependencies` VALUES (115, '嵌入式系统', '计算机系统', '7');
INSERT INTO `knowledge_dependencies` VALUES (116, '嵌入式系统', '专用功能', '7');
INSERT INTO `knowledge_dependencies` VALUES (117, '嵌入式系统', '硬件与软件集成', '7');
INSERT INTO `knowledge_dependencies` VALUES (118, '计算机系统', '硬件与软件集成', '7');
INSERT INTO `knowledge_dependencies` VALUES (119, 'ARM处理器', '处理器架构', '7');
INSERT INTO `knowledge_dependencies` VALUES (120, '嵌入式系统', 'ARM处理器', '7');
INSERT INTO `knowledge_dependencies` VALUES (121, '处理器架构', 'ARM处理器', '7');
INSERT INTO `knowledge_dependencies` VALUES (122, '处理器架构', '精简指令集计算（RISC）', '7');
INSERT INTO `knowledge_dependencies` VALUES (123, 'ARM处理器', '精简指令集计算（RISC）', '7');
INSERT INTO `knowledge_dependencies` VALUES (124, '嵌入式系统', '核心特征', '17');
INSERT INTO `knowledge_dependencies` VALUES (125, '嵌入式系统', '应用场景', '17');
INSERT INTO `knowledge_dependencies` VALUES (126, '嵌入式系统', '嵌入式系统的特点', '17');

-- ----------------------------
-- Table structure for knowledge_points
-- ----------------------------
DROP TABLE IF EXISTS `knowledge_points`;
CREATE TABLE `knowledge_points`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '关联的用户ID（UUID）',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name_user_id`(`name`, `user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 135 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of knowledge_points
-- ----------------------------
INSERT INTO `knowledge_points` VALUES (128, 'ARM处理器', '7');
INSERT INTO `knowledge_points` VALUES (99, 'I2C总线', '7');
INSERT INTO `knowledge_points` VALUES (118, 'Linux内核驱动开发', '7');
INSERT INTO `knowledge_points` VALUES (88, 'Linux系统', '7');
INSERT INTO `knowledge_points` VALUES (116, 'register_chrdev_region 函数', '7');
INSERT INTO `knowledge_points` VALUES (120, 'RTOS', '7');
INSERT INTO `knowledge_points` VALUES (97, 'SPI总线', '7');
INSERT INTO `knowledge_points` VALUES (106, 'USB接口', '7');
INSERT INTO `knowledge_points` VALUES (127, '专用功能', '7');
INSERT INTO `knowledge_points` VALUES (111, '专用系统功能', '7');
INSERT INTO `knowledge_points` VALUES (101, '串行通信', '7');
INSERT INTO `knowledge_points` VALUES (103, '主从通信', '7');
INSERT INTO `knowledge_points` VALUES (123, '传感器', '5');
INSERT INTO `knowledge_points` VALUES (98, '全双工通信方式', '7');
INSERT INTO `knowledge_points` VALUES (115, '内核功能工具', '7');
INSERT INTO `knowledge_points` VALUES (91, '内核编译', '7');
INSERT INTO `knowledge_points` VALUES (89, '内核配置', '7');
INSERT INTO `knowledge_points` VALUES (102, '同步通信', '7');
INSERT INTO `knowledge_points` VALUES (129, '处理器架构', '7');
INSERT INTO `knowledge_points` VALUES (96, '外设与接口', '7');
INSERT INTO `knowledge_points` VALUES (108, '外设支持', '7');
INSERT INTO `knowledge_points` VALUES (117, '字符设备注册', '7');
INSERT INTO `knowledge_points` VALUES (87, '定义', '7');
INSERT INTO `knowledge_points` VALUES (112, '实时性要求', '7');
INSERT INTO `knowledge_points` VALUES (121, '实时操作系统', '7');
INSERT INTO `knowledge_points` VALUES (90, '嵌入式Linux开发工具', '7');
INSERT INTO `knowledge_points` VALUES (131, '嵌入式系统', '17');
INSERT INTO `knowledge_points` VALUES (86, '嵌入式系统', '7');
INSERT INTO `knowledge_points` VALUES (109, '嵌入式系统定义', '7');
INSERT INTO `knowledge_points` VALUES (134, '嵌入式系统的特点', '17');
INSERT INTO `knowledge_points` VALUES (133, '应用场景', '17');
INSERT INTO `knowledge_points` VALUES (124, '微控制器', '5');
INSERT INTO `knowledge_points` VALUES (125, '接口类型', '5');
INSERT INTO `knowledge_points` VALUES (93, '操作系统移植', '7');
INSERT INTO `knowledge_points` VALUES (105, '数据线', '7');
INSERT INTO `knowledge_points` VALUES (122, '核心机制', '7');
INSERT INTO `knowledge_points` VALUES (132, '核心特征', '17');
INSERT INTO `knowledge_points` VALUES (114, '测试题目', '7');
INSERT INTO `knowledge_points` VALUES (94, '烧录过程', '7');
INSERT INTO `knowledge_points` VALUES (113, '硬件与软件集成', '7');
INSERT INTO `knowledge_points` VALUES (95, '硬件兼容性', '7');
INSERT INTO `knowledge_points` VALUES (92, '硬件架构', '7');
INSERT INTO `knowledge_points` VALUES (130, '精简指令集计算（RISC）', '7');
INSERT INTO `knowledge_points` VALUES (126, '计算机系统', '7');
INSERT INTO `knowledge_points` VALUES (110, '计算机系统基础', '7');
INSERT INTO `knowledge_points` VALUES (119, '设备号分配', '7');
INSERT INTO `knowledge_points` VALUES (107, '设备连接类型', '7');
INSERT INTO `knowledge_points` VALUES (104, '通信协议', '7');
INSERT INTO `knowledge_points` VALUES (100, '通信类型', '7');

-- ----------------------------
-- Table structure for practice_sessions
-- ----------------------------
DROP TABLE IF EXISTS `practice_sessions`;
CREATE TABLE `practice_sessions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_questions` int(11) NOT NULL,
  `correct_count` int(11) NOT NULL,
  `accuracy_rate` decimal(5, 2) NULL DEFAULT NULL,
  `score` int(11) NULL DEFAULT NULL,
  `session_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '练习会话ID（UUID）',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of practice_sessions
-- ----------------------------
INSERT INTO `practice_sessions` VALUES (7, 14, '单选题练习', 1, 1, 100.00, 100, '0444e5ed-917f-4a41-9933-202fd09134c4', '2025-07-06 09:56:08');
INSERT INTO `practice_sessions` VALUES (9, 15, '判断题练习', 1, 1, 100.00, 100, '359da3d2-8ff5-4c29-8722-6491632d4d40', '2025-07-06 09:58:00');
INSERT INTO `practice_sessions` VALUES (10, 7, '判断题练习', 1, 0, 0.00, 0, 'cdcce6dc-780b-47c7-9c17-dcaba76c56d9', '2025-07-06 09:58:15');
INSERT INTO `practice_sessions` VALUES (11, 7, '单选题练习', 3, 2, 66.67, 67, '61acf178-ffa5-48a1-8e3e-5338b627f100', '2025-07-06 09:58:42');
INSERT INTO `practice_sessions` VALUES (12, 5, '单选题练习', 1, 1, 100.00, 100, '45c05b84-a9e9-4e21-a2cd-cb1a5625675a', '2025-07-06 09:59:38');
INSERT INTO `practice_sessions` VALUES (13, 7, '单选题练习', 1, 0, 0.00, 0, '000985b3-f436-453c-9eb4-0f3ec13d80e9', '2025-07-16 09:43:24');
INSERT INTO `practice_sessions` VALUES (14, 7, '单选题练习', 1, 0, 0.00, 0, 'cdcee910-628b-4392-8277-d94cbedae2e7', '2025-07-20 11:57:09');
INSERT INTO `practice_sessions` VALUES (15, 7, '填空题练习', 1, 0, 0.00, 0, 'c8345501-48d1-435d-bb7c-60915528c529', '2025-07-21 15:27:06');
INSERT INTO `practice_sessions` VALUES (16, 7, '单选题练习', 1, 0, 100.00, 100, '5b397539-cbd8-4c34-b18b-f222c1cfd8b1', '2025-07-21 15:30:24');
INSERT INTO `practice_sessions` VALUES (17, 17, '单选题练习', 2, 0, 0.00, 0, '3ba1d60a-7606-43b4-a74f-48f542462c1b', '2025-07-21 16:07:27');

-- ----------------------------
-- Table structure for questions
-- ----------------------------
DROP TABLE IF EXISTS `questions`;
CREATE TABLE `questions`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `question_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `answer` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `difficulty` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `teacher_id` bigint(20) NULL DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 53 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of questions
-- ----------------------------
INSERT INTO `questions` VALUES (1, 'Q001', '简答题', '实现快速排序算法', 'public void quickSort(...)', '简单', '算法题库', 6, '2025-07-07 15:40:10');
INSERT INTO `questions` VALUES (2, 'Q002', '填空题', 'Spring Boot 默认使用的内嵌服务器是 ______。', 'Tomcat', '中等', '手动添加', 6, '2025-07-07 15:40:10');
INSERT INTO `questions` VALUES (3, 'Q003', '简答题', 'NFS 文件系统在嵌入式开发中有什么用途？', '可用于远程挂载根文件系统，便于调试和开发。', '困难', '手动添加', 6, '2025-07-07 15:40:10');
INSERT INTO `questions` VALUES (28, 'Q004', '单选题', '在嵌入式系统中，以下哪个是用于启动操作系统的程序？ A. Bootloader B. 内核 C. 应用程序 D. 驱动程序', 'A', '简单', 'AI生成', 6, '2025-07-07 15:40:10');
INSERT INTO `questions` VALUES (29, 'Q005', '单选题', 'Linux 中用于查看当前目录下文件和子目录的命令是？ A. ls B. cd C. pwd D. mkdir', 'A', '中等', 'AI生成', 6, '2025-07-07 15:40:10');
INSERT INTO `questions` VALUES (39, 'Q030', '单选题', '在嵌入式系统中，Bootloader 的主要作用是？ A. 管理文件系统 B. 提供图形界面 C. 加载并启动操作系统 D. 管理硬件设备', 'C', '简单', 'AI生成', 6, '2025-07-07 15:40:10');
INSERT INTO `questions` VALUES (40, 'Q031', '单选题', '在 Linux 中，用于查看当前系统运行进程的命令是？ A. ps -ef B. ls -l C. top D. df -h', 'A', '中等', 'AI生成', 6, '2025-07-07 15:40:10');
INSERT INTO `questions` VALUES (42, 'Q041', '单选题', 'Linux系统中，用于查看当前目录的命令是？ A. ls B. pwd C. cd D. mkdir', '4', '简单', 'AI生成', 7, '2025-07-09 23:13:10');
INSERT INTO `questions` VALUES (44, 'Q043', '判断题', '内核配置选项全部开启可以提高性能。()', '错误', '困难', 'AI生成', 7, '2025-07-09 23:24:25');
INSERT INTO `questions` VALUES (50, 'Q211883', '判断题', '\"进程间通信的常见方式包括管道、消息队列、共享内存等。\"()', '正确', '简单', 'AI生成', 21, '2025-07-22 00:59:52');
INSERT INTO `questions` VALUES (51, 'Q211830', '单选题', '以下哪种进程间通信方式最适合传输大量数据？ A. 管道 B. 消息队列 C. 共享内存 D. 信号', 'C', '困难', 'AI生成', 21, '2025-07-22 00:59:52');

-- ----------------------------
-- Table structure for teaching_efficiency
-- ----------------------------
DROP TABLE IF EXISTS `teaching_efficiency`;
CREATE TABLE `teaching_efficiency`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `teacher_id` bigint(20) NOT NULL,
  `date` date NOT NULL,
  `prep_time` int(11) NULL DEFAULT 0 COMMENT '备课时间(分钟)',
  `prep_revisions` int(11) NULL DEFAULT 0 COMMENT '备课修改次数',
  `optimization_notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '优化建议',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `teacher_date`(`teacher_id`, `date`) USING BTREE,
  CONSTRAINT `teaching_efficiency_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of teaching_efficiency
-- ----------------------------
INSERT INTO `teaching_efficiency` VALUES (3, 6, '2025-07-02', 120, 3, '需要增加更多练习环节');
INSERT INTO `teaching_efficiency` VALUES (7, 7, '2023-11-23', 120, 4, '对练习进行及时复习，指出错误原因');
INSERT INTO `teaching_efficiency` VALUES (8, 6, '2025-07-18', 10, 4, '多做相似题目，找出解题技巧');
INSERT INTO `teaching_efficiency` VALUES (9, 9, '2023-12-01', 0, 0, '注意基础知识点');
INSERT INTO `teaching_efficiency` VALUES (10, 9, '2025-04-05', 3, 2, '掌握核心用法');
INSERT INTO `teaching_efficiency` VALUES (12, 7, '2025-07-14', 118, 1, '做题要审清题目');
INSERT INTO `teaching_efficiency` VALUES (13, 7, '2025-07-15', 574, 0, '避免马虎，看题目要仔细');
INSERT INTO `teaching_efficiency` VALUES (15, 21, '2025-07-21', 281, 45, '多做题，细心');

-- ----------------------------
-- Table structure for teaching_materials
-- ----------------------------
DROP TABLE IF EXISTS `teaching_materials`;
CREATE TABLE `teaching_materials`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `resource_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '资源名称',
  `file_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文件类型（PDF/PPTX/DOCX等）',
  `teacher_id` bigint(20) NOT NULL COMMENT '创建教师ID',
  `file_size` int(11) NOT NULL COMMENT '文件大小（字节）',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `file_path` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文件存储路径',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 69 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of teaching_materials
-- ----------------------------
INSERT INTO `teaching_materials` VALUES (7, '软件构造试卷', 'PDF', 6, 3072, '2025-07-09 14:24:25', 'exam.pdf');
INSERT INTO `teaching_materials` VALUES (45, '标准答案_20250715_191352', 'DOCX', 7, 168807, '2025-07-15 19:14:24', '标准答案_20250715_191352.docx');
INSERT INTO `teaching_materials` VALUES (47, '标准答案_20250715_192629', 'DOCX', 7, 38746, '2025-07-15 19:27:00', '标准答案_20250715_192629.docx');
INSERT INTO `teaching_materials` VALUES (48, '评分标准_20250715_192629', 'DOCX', 7, 38356, '2025-07-15 19:27:00', '评分标准_20250715_192629.docx');
INSERT INTO `teaching_materials` VALUES (49, '高等数学_20250715_193610_试卷分析表', 'DOCX', 7, 90004, '2025-07-15 19:36:10', '高等数学_20250715_193610_试卷分析表.docx');
INSERT INTO `teaching_materials` VALUES (51, 'teaching_plan_20250716_003248', 'TXT', 7, 1169, '2025-07-16 00:32:48', 'teaching_plan_20250716_003248.txt');
INSERT INTO `teaching_materials` VALUES (52, 'teaching_plan_20250716_173215', 'TXT', 7, 2115, '2025-07-16 17:32:15', 'teaching_plan_20250716_173215.txt');
INSERT INTO `teaching_materials` VALUES (53, '标准答案_20250716_173532', 'DOCX', 7, 38809, '2025-07-16 17:36:08', '标准答案_20250716_173532.docx');
INSERT INTO `teaching_materials` VALUES (54, '评分标准_20250716_173532', 'DOCX', 7, 38514, '2025-07-16 17:36:08', '评分标准_20250716_173532.docx');
INSERT INTO `teaching_materials` VALUES (55, '高等数学_20250716_173632_试卷分析表', 'DOCX', 7, 90701, '2025-07-16 17:36:32', '高等数学_20250716_173632_试卷分析表.docx');
INSERT INTO `teaching_materials` VALUES (56, 'teaching_plan_20250719_233845', 'TXT', 7, 1644, '2025-07-19 23:38:46', 'teaching_plan_20250719_233845.txt');
INSERT INTO `teaching_materials` VALUES (57, '标准答案_20250721_234128', 'DOCX', 7, 38848, '2025-07-21 23:41:58', '标准答案_20250721_234128.docx');
INSERT INTO `teaching_materials` VALUES (58, '评分标准_20250721_234128', 'DOCX', 7, 38466, '2025-07-21 23:41:58', '评分标准_20250721_234128.docx');
INSERT INTO `teaching_materials` VALUES (59, '软件构造_20250721_234256_试卷分析表', 'DOCX', 7, 91051, '2025-07-21 23:42:57', '软件构造_20250721_234256_试卷分析表.docx');
INSERT INTO `teaching_materials` VALUES (60, 'teaching_plan_20250722_001140', 'TXT', 18, 1773, '2025-07-22 00:11:40', 'teaching_plan_20250722_001140.txt');
INSERT INTO `teaching_materials` VALUES (61, 'teaching_plan_20250722_004736', 'TXT', 20, 1190, '2025-07-22 00:47:37', 'teaching_plan_20250722_004736.txt');
INSERT INTO `teaching_materials` VALUES (62, '标准答案_20250722_005001', 'DOCX', 20, 38853, '2025-07-22 00:50:32', '标准答案_20250722_005001.docx');
INSERT INTO `teaching_materials` VALUES (63, '评分标准_20250722_005001', 'DOCX', 20, 38247, '2025-07-22 00:50:32', '评分标准_20250722_005001.docx');
INSERT INTO `teaching_materials` VALUES (64, '软件构造_20250722_005124_试卷分析表', 'DOCX', 20, 90873, '2025-07-22 00:51:25', '软件构造_20250722_005124_试卷分析表.docx');
INSERT INTO `teaching_materials` VALUES (65, 'teaching_plan_20250722_005901', 'TXT', 21, 1853, '2025-07-22 00:59:01', 'teaching_plan_20250722_005901.txt');
INSERT INTO `teaching_materials` VALUES (66, '标准答案_20250722_010114', 'DOCX', 21, 38838, '2025-07-22 01:01:40', '标准答案_20250722_010114.docx');
INSERT INTO `teaching_materials` VALUES (67, '评分标准_20250722_010114', 'DOCX', 21, 38305, '2025-07-22 01:01:40', '评分标准_20250722_010114.docx');
INSERT INTO `teaching_materials` VALUES (68, '软件构造_20250722_010223_试卷分析表', 'DOCX', 21, 91081, '2025-07-22 01:02:23', '软件构造_20250722_010223_试卷分析表.docx');

-- ----------------------------
-- Table structure for user_answers
-- ----------------------------
DROP TABLE IF EXISTS `user_answers`;
CREATE TABLE `user_answers`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '题目类型（choice/judge/fill/essay）',
  `question_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '题目内容（含选项）',
  `difficulty` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '难度等级（easy/medium/hard）',
  `user_answer` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '用户提交的答案',
  `correct_answer` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '标准答案',
  `explanation` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '解析说明',
  `is_correct` tinyint(1) NULL DEFAULT 0 COMMENT '是否正确',
  `answered_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `session_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `user_id` bigint(20) NOT NULL COMMENT '学生用户ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 112 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_answers
-- ----------------------------
INSERT INTO `user_answers` VALUES (80, 'choice', '在嵌入式Linux系统中，以下哪一项是用于配置内核功能的工具？', '中等', 'C', 'C', '回答正确。在嵌入式Linux系统中，\'make menuconfig\' 是用于配置内核功能的工具。它提供了一个基于文本的交互式菜单界面，允许用户选择和配置内核的各个功能模块。', 1, '2025-07-06 17:55:48', '0444e5ed-917f-4a41-9933-202fd09134c4', 14);
INSERT INTO `user_answers` VALUES (81, 'judge', '\"内核编译完成后，可以直接烧录到任意硬件上运行。\"()', '中等', 'false', 'false', '回答正确。内核编译完成后，需要根据具体的硬件平台进行适配，不能直接烧录到任意硬件上运行。不同的硬件平台可能有不同的启动方式、设备驱动和配置需求。', 1, '2025-07-06 17:57:52', '359da3d2-8ff5-4c29-8722-6491632d4d40', 15);
INSERT INTO `user_answers` VALUES (82, 'judge', '\"外设与接口中的SPI总线是全双工通信方式。\"()', '中等', 'true', 'false', '回答错误。SPI总线是半双工通信方式，虽然它支持数据的双向传输，但同一时间只能在一个方向上传输数据，因此不是全双工通信方式。', 0, '2025-07-06 17:58:07', 'cdcce6dc-780b-47c7-9c17-dcaba76c56d9', 7);
INSERT INTO `user_answers` VALUES (83, 'choice', 'I2C总线主要用于哪种类型的通信？', '中等', 'B', 'B', '回答正确。I2C总线是一种串行总线，用于设备之间的低速通信，通常用于连接传感器、EEPROM等外设。选项B（串行总线）是正确答案。', 1, '2025-07-06 17:58:26', '61acf178-ffa5-48a1-8e3e-5338b627f100', 7);
INSERT INTO `user_answers` VALUES (84, 'choice', '在嵌入式系统中，SPI总线通常使用多少根数据线进行通信？', '中等', 'B', 'D', '回答错误。SPI总线通常使用4根数据线进行通信，包括SCLK（时钟线）、MOSI（主出从入）、MISO（主入从出）和SS（片选线）。选项D表示4根数据线，因此正确答案是D。', 0, '2025-07-06 17:58:26', '61acf178-ffa5-48a1-8e3e-5338b627f100', 7);
INSERT INTO `user_answers` VALUES (85, 'choice', 'USB接口支持哪种类型的设备连接？', '中等', 'A', 'A', '回答正确。USB接口支持外设的连接，如键盘、鼠标、打印机等。USB是一种通用串行总线，用于连接各种外部设备与计算机或嵌入式系统。', 1, '2025-07-02 17:58:26', '61acf178-ffa5-48a1-8e3e-5338b627f100', 7);
INSERT INTO `user_answers` VALUES (86, 'choice', '以下哪种处理器架构采用了精简指令集？', '中等', 'B', 'B', '回答正确。精简指令集（RISC）是一种设计哲学，旨在通过减少指令集的复杂性来提高处理器性能。ARM 处理器就是基于 RISC 架构的典型代表。选项 A 表示 RISC，因此是正确答案。', 1, '2025-07-07 17:59:32', '45c05b84-a9e9-4e21-a2cd-cb1a5625675a', 5);
INSERT INTO `user_answers` VALUES (87, 'choice', '以下哪一项最准确地描述了嵌入式系统的定义？', '困难', 'B', 'D', '回答错误。嵌入式系统的定义是：以应用为中心，以计算机技术为基础，软硬件可剪裁，适用于对功能、可靠性、成本、体积、功耗等有严格要求的专用计算机系统。选项D最准确地描述了这一定义。选项B可能指的是嵌入式系统的某个特点或应用场景，但不是其核心定义。', 0, '2025-07-16 17:42:49', '000985b3-f436-453c-9eb4-0f3ec13d80e9', 7);
INSERT INTO `user_answers` VALUES (106, 'choice', '在Linux内核编译过程中，以下哪个文件用于配置内核选项？', '中等', 'C', 'A', '回答错误。在Linux内核编译过程中，用于配置内核选项的文件是 .config 文件，而不是 C 文件。.config 文件存储了内核的配置参数，是编译过程中重要的配置文件。', 0, '2025-07-20 19:57:02', 'cdcee910-628b-4392-8277-d94cbedae2e7', 7);
INSERT INTO `user_answers` VALUES (107, 'choice', '以下哪项最准确地描述了嵌入式系统的定义？', '困难', 'D', 'A', '回答错误。嵌入式系统的定义是：以应用为中心，以计算机技术为基础，软硬件可裁剪，适用于对功能、可靠性、成本、体积、功耗等有严格要求的专用计算机系统。选项 A 是最准确的描述，而选项 D 不符合嵌入式系统的定义。', 0, '2025-07-21 21:23:03', '678d707b-485b-43de-8933-9a87b14f125f', 7);
INSERT INTO `user_answers` VALUES (108, 'fill', 'ARM 处理器是嵌入式领域常用的______架构处理器。', '简单', '[\"0\"]', 'RISC', '回答错误。ARM 处理器是基于 RISC（精简指令集）架构的处理器，而不是数字 0。请复习嵌入式系统概述中关于处理器架构的内容。', 0, '2025-07-21 23:25:18', 'c8345501-48d1-435d-bb7c-60915528c529', 7);
INSERT INTO `user_answers` VALUES (109, 'choice', 'ARM 处理器属于哪种架构？', '简单', 'A', 'A', '回答正确。ARM 处理器属于 RISC 架构，而不是 CISC。RISC（精简指令集）架构的特点是指令集简单、执行速度快，而 CISC（复杂指令集）架构则指令集复杂、功能强大但执行速度相对较慢。', 1, '2025-07-21 23:30:14', '5b397539-cbd8-4c34-b18b-f222c1cfd8b1', 7);
INSERT INTO `user_answers` VALUES (110, 'choice', '以下哪项是嵌入式系统的核心特征？', '中等', 'B', 'D', '回答错误。嵌入式系统的核心特征是专用性强，而不是通用性强。选项 D 表示通用性强，这与嵌入式系统的定义相违背。嵌入式系统通常是为特定功能设计的，资源受限，并且具有实时性。', 0, '2025-07-22 00:07:03', '3ba1d60a-7606-43b4-a74f-48f542462c1b', 17);
INSERT INTO `user_answers` VALUES (111, 'choice', '嵌入式系统通常用于以下哪种场景？', '中等', 'D', 'A', '回答错误。嵌入式系统通常用于资源受限的环境中，例如工业控制、家电控制器、智能设备等。选项A（智能手机）是嵌入式系统的典型应用之一。而选项D可能指的是通用计算机，这不属于嵌入式系统的典型应用场景。', 0, '2025-07-22 00:07:03', '3ba1d60a-7606-43b4-a74f-48f542462c1b', 17);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `nickname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (5, 'student1', '小明', '123456', 'student');
INSERT INTO `users` VALUES (6, 'teacher1', '教师A', '123456', 'teacher');
INSERT INTO `users` VALUES (7, 'admin1', '测试用户', '123456', 'admin');
INSERT INTO `users` VALUES (8, 'student2', '小红', '123456', 'student');
INSERT INTO `users` VALUES (9, 'teacher2', '教师B', '123456', 'teacher');
INSERT INTO `users` VALUES (14, '2222', '测试用户1', '123456', 'student');
INSERT INTO `users` VALUES (15, '111', '测试用户2', '123456', 'student');
INSERT INTO `users` VALUES (17, 'student001', '小华', '123456', 'student');
INSERT INTO `users` VALUES (21, 'teacher001', '李老师', 'l123456', 'teacher');

-- ----------------------------
-- Procedure structure for analyze_knowledge
-- ----------------------------
DROP PROCEDURE IF EXISTS `analyze_knowledge`;
delimiter ;;
CREATE PROCEDURE `analyze_knowledge`(IN answer_id INT)
BEGIN
    DECLARE question_content TEXT;

    -- 获取题目内容
    SELECT question_content INTO question_content 
    FROM user_answers 
    WHERE id = answer_id;

    -- 假设分析出3个知识点
    INSERT IGNORE INTO knowledge_points (name) VALUES 
    (CONCAT('知识点-', FLOOR(RAND()*100))),
    (CONCAT('知识点-', FLOOR(RAND()*100))),
    (CONCAT('知识点-', FLOOR(RAND()*100)));
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
