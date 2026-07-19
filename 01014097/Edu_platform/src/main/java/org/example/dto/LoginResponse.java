package org.example.dto;

import lombok.Data;

@Data
public class LoginResponse {
    private Long id;
    private String username;
    private String nickname;  // 新增字段
    private String role;
}