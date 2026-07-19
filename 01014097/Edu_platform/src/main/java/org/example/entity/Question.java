package org.example.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Entity
@Table(name = "questions")
@Data
public class Question {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "question_id", nullable = false, length = 50, unique = true)
    private String questionId;

    @Column(nullable = false, length = 100)
    private String type;

    @Column(name = "question_type", length = 50)
    private String questionType;

    @Column(columnDefinition = "TEXT", nullable = false)
    private String content;

    @Column(columnDefinition = "TEXT", nullable = false)
    private String answer;

    @Column(nullable = false, length = 50)
    private String difficulty;

    @Column(length = 100)
    private String source;

    @Column(name = "knowledge_point", length = 255)
    private String knowledgePoint;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();
}