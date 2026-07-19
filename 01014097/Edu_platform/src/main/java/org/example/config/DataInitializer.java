package org.example.config;

import org.example.entity.User;
import org.example.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DataInitializer {

    @Autowired
    private UserRepository userRepository;

    @Bean
    public ApplicationRunner initData() {
        return args -> {
            // 检查是否已有用户数据
            if (userRepository.count() == 0) {
                // 创建管理员用户
                User admin = new User();
                admin.setUsername("admin");
                admin.setPassword("admin123");
                admin.setRole("admin");
                admin.setNickname("管理员");
                userRepository.save(admin);

                // 创建教师用户
                User teacher = new User();
                teacher.setUsername("teacher");
                teacher.setPassword("teacher123");
                teacher.setRole("teacher");
                teacher.setNickname("教师");
                userRepository.save(teacher);

                // 创建学生用户
                User student = new User();
                student.setUsername("student");
                student.setPassword("student123");
                student.setRole("student");
                student.setNickname("学生");
                userRepository.save(student);

                System.out.println("初始用户数据已创建");
            }
        };
    }
}