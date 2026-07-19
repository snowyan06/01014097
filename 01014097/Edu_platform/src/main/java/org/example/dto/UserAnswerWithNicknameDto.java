// src/main/java/org/example/dto/UserAnswerWithNicknameDto.java
package org.example.dto;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class UserAnswerWithNicknameDto {
    private Integer id;
    private String questionType;
    private String questionContent;
    private String difficulty;
    private String userAnswer;
    private String correctAnswer;
    private String explanation;
    private Boolean isCorrect;
    private LocalDateTime answeredAt;
    private String sessionId;
    private Long userId;
    private String nickname;

    // 用于 JPQL 查询的构造函数
    public UserAnswerWithNicknameDto(
            Integer id, String questionType, String questionContent,
            String difficulty, String userAnswer, String correctAnswer,
            String explanation, Boolean isCorrect, LocalDateTime answeredAt,
            String sessionId, Long userId, String nickname) {
        this.id = id;
        this.questionType = questionType;
        this.questionContent = questionContent;
        this.difficulty = difficulty;
        this.userAnswer = userAnswer;
        this.correctAnswer = correctAnswer;
        this.explanation = explanation;
        this.isCorrect = isCorrect;
        this.answeredAt = answeredAt;
        this.sessionId = sessionId;
        this.userId = userId;
        this.nickname = nickname;
    }
}