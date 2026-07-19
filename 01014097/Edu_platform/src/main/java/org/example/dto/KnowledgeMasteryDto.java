// src/main/java/org/example/dto/KnowledgeMasteryDto.java
package org.example.dto;

public class KnowledgeMasteryDto {
    private String questionType;
    private Integer totalQuestions;
    private Integer correctAnswers;
    private Double masteryRate;

    // 构造方法
    public KnowledgeMasteryDto(String questionType, Integer totalQuestions, Integer correctAnswers, Double masteryRate) {
        this.questionType = questionType;
        this.totalQuestions = totalQuestions;
        this.correctAnswers = correctAnswers;
        this.masteryRate = masteryRate;
    }

    // Getter和Setter方法
    public String getQuestionType() {
        return questionType;
    }

    public void setQuestionType(String questionType) {
        this.questionType = questionType;
    }

    public Integer getTotalQuestions() {
        return totalQuestions;
    }

    public void setTotalQuestions(Integer totalQuestions) {
        this.totalQuestions = totalQuestions;
    }

    public Integer getCorrectAnswers() {
        return correctAnswers;
    }

    public void setCorrectAnswers(Integer correctAnswers) {
        this.correctAnswers = correctAnswers;
    }

    public Double getMasteryRate() {
        return masteryRate;
    }

    public void setMasteryRate(Double masteryRate) {
        this.masteryRate = masteryRate;
    }
}