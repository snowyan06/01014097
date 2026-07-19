// src/main/java/org/example/dto/UserAnswerStatsDto.java
package org.example.dto;

import lombok.Data;

@Data
public class UserAnswerStatsDto {
    private Long userId;
    private Long count;
    private String nickname;

    // 用于 JPQL 查询的构造函数
    public UserAnswerStatsDto(Long userId, Long count, String nickname) {
        this.userId = userId;
        this.count = count;
        this.nickname = nickname;
    }
}