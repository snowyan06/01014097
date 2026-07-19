package org.example.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Entity
@Data
@Table(name = "user_answers")
public class UserAnswer {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "question_type", nullable = false, length = 20)
    private String questionType;

    @Column(name = "question_content", nullable = false, columnDefinition = "TEXT")
    private String questionContent;

    @Column(nullable = false, length = 10)
    private String difficulty;

    // 允许为空的字段开始
    @Column(name = "user_answer", nullable = true, columnDefinition = "TEXT")
    private String userAnswer;

    @Column(name = "correct_answer", nullable = true, columnDefinition = "TEXT")
    private String correctAnswer;

    @Column(columnDefinition = "TEXT")
    private String explanation;

    @Column(name = "is_correct", nullable = true)
    private Boolean isCorrect;

    @Column(name = "answered_at")
    private LocalDateTime answeredAt = LocalDateTime.now();

    @Column(name = "session_id", length = 36)
    private String sessionId;

    @Column(name = "user_id", nullable = false, length = 36)
    private Long userId;
}