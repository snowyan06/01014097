package org.example.dto;

import lombok.Data;

@Data
public class UserProfileResponse {
    private Long id;
    private String username;
    private String nickname;
    private String email;
    private String avatar;
    private String role;

    public UserProfileResponse() {}

    public UserProfileResponse(Long id, String username, String nickname, String email, String avatar, String role) {
        this.id = id;
        this.username = username;
        this.nickname = nickname;
        this.email = email;
        this.avatar = avatar;
        this.role = role;
    }
}
