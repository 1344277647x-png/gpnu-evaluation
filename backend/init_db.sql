-- ============================================
-- 公选课教师评价系统 数据库初始化
-- MySQL 8.0+
-- ============================================

CREATE DATABASE IF NOT EXISTS gpnu_evaluation
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE gpnu_evaluation;

-- --------------------------------------------
-- 用户表
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  nickname VARCHAR(50) NOT NULL,
  student_id VARCHAR(20) NOT NULL,
  role ENUM('student','admin') NOT NULL DEFAULT 'student',
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------
-- 分类表
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS categories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  sort_order INT NOT NULL DEFAULT 0,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  UNIQUE INDEX idx_category_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------
-- 教师表
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS teachers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  department VARCHAR(100) NOT NULL DEFAULT '',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------
-- 课程表
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS courses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  teacher_id INT NOT NULL,
  category_id INT NOT NULL,
  semester VARCHAR(20) NOT NULL DEFAULT '',
  description TEXT,
  status ENUM('pending','approved','rejected','inactive') NOT NULL DEFAULT 'pending',
  reject_reason VARCHAR(500) DEFAULT NULL,
  created_by INT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE INDEX idx_course_unique (name, teacher_id, semester),
  INDEX idx_course_status (status),
  INDEX idx_course_teacher (teacher_id),
  INDEX idx_course_category (category_id),
  INDEX idx_course_created (created_at),
  CONSTRAINT fk_course_teacher FOREIGN KEY (teacher_id) REFERENCES teachers(id),
  CONSTRAINT fk_course_category FOREIGN KEY (category_id) REFERENCES categories(id),
  CONSTRAINT fk_course_user FOREIGN KEY (created_by) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------
-- 评价表
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS reviews (
  id INT AUTO_INCREMENT PRIMARY KEY,
  course_id INT NOT NULL,
  user_id INT NOT NULL,
  rating_teaching TINYINT NOT NULL CHECK (rating_teaching BETWEEN 1 AND 5),
  rating_content TINYINT NOT NULL CHECK (rating_content BETWEEN 1 AND 5),
  rating_exam TINYINT NOT NULL CHECK (rating_exam BETWEEN 1 AND 5),
  rating_fairness TINYINT NOT NULL CHECK (rating_fairness BETWEEN 1 AND 5),
  comment TEXT,
  is_hidden TINYINT(1) NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE INDEX idx_review_unique (user_id, course_id),
  INDEX idx_review_course (course_id, created_at),
  CONSTRAINT fk_review_course FOREIGN KEY (course_id) REFERENCES courses(id),
  CONSTRAINT fk_review_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------
-- 预设数据
-- --------------------------------------------

-- 分类
INSERT INTO categories (name, sort_order) VALUES
  ('人文社科', 1),
  ('自然科学', 2),
  ('工程技术', 3),
  ('艺术体育', 4),
  ('其他', 5);

-- 默认管理员 (密码: Admin123456, bcrypt hash)
-- 实际运行时由 Python 生成 hash，此处占位
INSERT INTO users (username, password_hash, nickname, student_id, role) VALUES
  ('admin', '$2b$12$LJ3m4ys3Lk0TSwHCpNqrveDQFWuxBTVZ3XxDZfXt1J5wfTCcIsYlS', '系统管理员', '000000', 'admin');

-- 预设教师
INSERT INTO teachers (name, department) VALUES
  ('张明远', '人文学院'),
  ('李秀华', '理学院'),
  ('王建国', '工学院'),
  ('陈思雨', '艺术学院'),
  ('刘文博', '体育学院'),
  ('赵晓峰', '教育学院'),
  ('黄丽萍', '外语学院');

-- 示例课程
INSERT INTO courses (name, teacher_id, category_id, semester, description, status, created_by) VALUES
  ('中国传统文化概论', 1, 1, '2025-2026-2', '探讨中国传统文化的核心思想与当代价值，涵盖儒家、道家、佛家等多元文化脉络。', 'approved', 1),
  ('生活中的化学', 2, 2, '2025-2026-2', '从日常生活出发，讲解化学原理在衣食住行中的应用，无需化学基础。', 'approved', 1),
  ('Python编程入门', 3, 3, '2025-2026-2', '零基础学Python，从变量到函数，动手编写实用小程序。', 'approved', 1),
  ('摄影艺术与审美', 4, 4, '2025-2026-2', '学习构图、光影、色彩理论，用镜头发现生活中的美。', 'approved', 1),
  ('篮球技战术', 5, 4, '2025-2026-2', '系统学习篮球基本技术和战术配合，以赛代练提升实战能力。', 'approved', 1),
  ('教育心理学', 6, 1, '2025-2026-2', '了解学习心理、动机理论和课堂管理策略，适合未来从事教育工作的同学。', 'approved', 1),
  ('日本语言与文化', 7, 1, '2025-2026-2', '从五十音图到日常会话，结合动漫、影视了解日本文化。', 'approved', 1);

-- AI chat message logs
CREATE TABLE IF NOT EXISTS chat_messages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  session_id VARCHAR(64) NOT NULL,
  user_id INT NULL,
  role VARCHAR(20) NOT NULL,
  content TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_chat_session (session_id, created_at),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);
