package org.example.service;

import org.example.dto.UserCreateRequest;
import org.example.dto.UserUpdateRequest;
import org.example.entity.User;
import org.example.exception.DuplicateUsernameException;
import org.example.exception.NotFoundException;
import org.example.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UserService {

    private final UserRepository userRepository;

    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public User createUser(UserCreateRequest request) {
        if (userRepository.findByUsername(request.getUsername()).isPresent()) {
            throw new DuplicateUsernameException("用户名已存在");
        }

        User user = new User();
        user.setUsername(request.getUsername());
        user.setPassword(request.getPassword()); // 不再加密
        user.setRole(request.getRole());
        user.setNickname(request.getNickname());

        return userRepository.save(user);
    }

    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    public User getUserById(Long id) {
        return userRepository.findById(id)
                .orElseThrow(() -> new NotFoundException("用户不存在"));
    }

    public User updateUser(Long id, UserUpdateRequest request) {
        System.out.println("UserService.updateUser 被调用，用户 ID: " + id);
        User user = getUserById(id);
        
        System.out.println("原始用户数据 - username: " + user.getUsername());

        if (request.getPassword() != null) {
            user.setPassword(request.getPassword());
            System.out.println("更新 password");
        }
        if (request.getRole() != null) {
            user.setRole(request.getRole());
            System.out.println("更新 role");
        }
        if (request.getNickname() != null) {
            user.setNickname(request.getNickname());
            System.out.println("更新 nickname: " + request.getNickname());
        }
        if (request.getEmail() != null) {
            user.setEmail(request.getEmail());
            System.out.println("更新 email: " + request.getEmail());
        }
        if (request.getAvatar() != null) {
            System.out.println("更新 avatar，长度：" + request.getAvatar().length());
            user.setAvatar(request.getAvatar());
        }
        
        System.out.println("保存用户信息...");
        User savedUser = userRepository.save(user);
        System.out.println("用户信息保存成功，新 ID: " + savedUser.getId());
        
        return savedUser;
    }

    public void deleteUser(Long id) {
        if (!userRepository.existsById(id)) {
            throw new NotFoundException("用户不存在");
        }
        userRepository.deleteById(id);
    }

    public List<User> getTeachersAndAdmins() {
        return userRepository.findTeachersAndAdmins();
    }

    public List<User> getUsersByRole(String role) {
        return userRepository.findByRole(role);
    }
}