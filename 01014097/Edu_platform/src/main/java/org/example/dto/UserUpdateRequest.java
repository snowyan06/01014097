package org.example.dto;

import lombok.Data;

@Data
public class UserUpdateRequest {
    private String password;
    private String role;
    private String nickname;
    private String email;
    private String avatar;
}