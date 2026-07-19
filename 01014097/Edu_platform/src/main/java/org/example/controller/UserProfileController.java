package org.example.controller;

import org.example.dto.UserProfileResponse;
import org.example.dto.UserUpdateRequest;
import org.example.entity.User;
import org.example.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.Base64;
import java.util.regex.Pattern;

@RestController
@RequestMapping("/api/user")
@CrossOrigin(origins = "*")
public class UserProfileController {

    @Autowired
    private UserService userService;

    private static final Pattern EMAIL_PATTERN = Pattern.compile(
        "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$"
    );

    @GetMapping("/profile/{userId}")
    public ResponseEntity<UserProfileResponse> getUserProfile(@PathVariable("userId") Long userId) {
        User user = userService.getUserById(userId);
        
        UserProfileResponse response = new UserProfileResponse();
        response.setId(user.getId());
        response.setUsername(user.getUsername());
        response.setNickname(user.getNickname());
        response.setEmail(user.getEmail());
        response.setAvatar(user.getAvatar());
        response.setRole(user.getRole());
        
        return ResponseEntity.ok(response);
    }

    @PutMapping("/profile/{userId}")
    public ResponseEntity<UserProfileResponse> updateUserProfile(
            @PathVariable("userId") Long userId,
            @RequestBody UserUpdateRequest request) {
        
        if (request.getEmail() != null && !request.getEmail().isEmpty()) {
            if (!EMAIL_PATTERN.matcher(request.getEmail()).matches()) {
                throw new IllegalArgumentException("邮箱格式不正确");
            }
        }
        
        User updatedUser = userService.updateUser(userId, request);
        
        UserProfileResponse response = new UserProfileResponse();
        response.setId(updatedUser.getId());
        response.setUsername(updatedUser.getUsername());
        response.setNickname(updatedUser.getNickname());
        response.setEmail(updatedUser.getEmail());
        response.setAvatar(updatedUser.getAvatar());
        response.setRole(updatedUser.getRole());
        
        return ResponseEntity.ok(response);
    }

    @PostMapping("/avatar/{userId}")
    public ResponseEntity<UserProfileResponse> uploadAvatar(
            @PathVariable("userId") Long userId,
            @RequestParam("avatar") MultipartFile file) {
        
        System.out.println("=== 开始上传头像 ===");
        System.out.println("用户 ID: " + userId);
        System.out.println("文件名：" + file.getOriginalFilename());
        System.out.println("文件大小：" + file.getSize() + " bytes");
        System.out.println("文件类型：" + file.getContentType());
        
        if (file.isEmpty()) {
            throw new IllegalArgumentException("上传文件不能为空");
        }
        
        String contentType = file.getContentType();
        if (contentType == null || !contentType.startsWith("image/")) {
            throw new IllegalArgumentException("只能上传图片文件");
        }
        
        long maxSize = 2 * 1024 * 1024;
        if (file.getSize() > maxSize) {
            throw new IllegalArgumentException("图片大小不能超过 2MB");
        }
        
        try {
            byte[] imageBytes = file.getBytes();
            System.out.println("图片字节数：" + imageBytes.length);
            
            String base64Avatar = Base64.getEncoder().encodeToString(imageBytes);
            System.out.println("Base64 长度：" + base64Avatar.length());
            
            String dataUrl = "data:" + contentType + ";base64," + base64Avatar;
            
            UserUpdateRequest request = new UserUpdateRequest();
            request.setAvatar(dataUrl);
            
            System.out.println("准备更新用户信息...");
            User updatedUser = userService.updateUser(userId, request);
            System.out.println("用户信息更新成功");
            
            UserProfileResponse response = new UserProfileResponse();
            response.setId(updatedUser.getId());
            response.setUsername(updatedUser.getUsername());
            response.setNickname(updatedUser.getNickname());
            response.setEmail(updatedUser.getEmail());
            response.setAvatar(updatedUser.getAvatar());
            response.setRole(updatedUser.getRole());
            
            System.out.println("=== 头像上传完成 ===");
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            System.err.println("头像上传异常：" + e.getMessage());
            e.printStackTrace();
            throw new RuntimeException("头像上传失败：" + e.getMessage());
        }
    }
}
