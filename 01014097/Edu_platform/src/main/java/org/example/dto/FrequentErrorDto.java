// src/main/java/org/example/dto/FrequentErrorDto.java
package org.example.dto;

public class FrequentErrorDto {
    private String questionContent;
    private String questionType;
    private String difficulty;
    private Integer errorCount;
    private String correctAnswer;
    private String explanation;

    // 构造方法
    public FrequentErrorDto(String questionContent, String questionType, String difficulty,
                            Integer errorCount, String correctAnswer, String explanation) {
        this.questionContent = questionContent;
        this.questionType = questionType;
        this.difficulty = difficulty;
        this.errorCount = errorCount;
        this.correctAnswer = correctAnswer;
        this.explanation = explanation;
    }

    // Getter和Setter方法
    public String getQuestionContent() {
        return questionContent;
    }

    public void setQuestionContent(String questionContent) {
        this.questionContent = questionContent;
    }

    public String getQuestionType() {
        return questionType;
    }

    public void setQuestionType(String questionType) {
        this.questionType = questionType;
    }

    public String getDifficulty() {
        return difficulty;
    }

    public void setDifficulty(String difficulty) {
        this.difficulty = difficulty;
    }

    public Integer getErrorCount() {
        return errorCount;
    }

    public void setErrorCount(Integer errorCount) {
        this.errorCount = errorCount;
    }

    public String getCorrectAnswer() {
        return correctAnswer;
    }

    public void setCorrectAnswer(String correctAnswer) {
        this.correctAnswer = correctAnswer;
    }

    public String getExplanation() {
        return explanation;
    }

    public void setExplanation(String explanation) {
        this.explanation = explanation;
    }
}