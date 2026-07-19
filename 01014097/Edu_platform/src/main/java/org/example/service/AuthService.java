package org.example.service;

import org.example.entity.User;
import org.example.exception.AuthenticationException;
import org.example.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    @Autowired
    private UserRepository userRepository;

    public User authenticate(String username, String password, String role) {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new AuthenticationException("用户名或密码错误"));

        // 简化版：直接比较密码（实际项目中应该加密比较）
        if (!user.getPassword().equals(password)) {
            throw new AuthenticationException("用户名或密码错误");
        }

        if (!user.getRole().equalsIgnoreCase(role)) {
            throw new AuthenticationException("您没有权限以" + role + "身份登录");
        }

        return user;
    }
}