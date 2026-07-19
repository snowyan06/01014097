// src/main/java/org/example/dto/CorrectRateTrendDto.java
package org.example.dto;

import java.time.LocalDate;

public class CorrectRateTrendDto {
    private LocalDate date;
    private Integer totalAnswers;
    private Integer correctAnswers;
    private Double correctRate;

    // 构造方法
    public CorrectRateTrendDto(LocalDate date, Integer totalAnswers, Integer correctAnswers, Double correctRate) {
        this.date = date;
        this.totalAnswers = totalAnswers;
        this.correctAnswers = correctAnswers;
        this.correctRate = correctRate;
    }

    // Getter和Setter方法
    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public Integer getTotalAnswers() {
        return totalAnswers;
    }

    public void setTotalAnswers(Integer totalAnswers) {
        this.totalAnswers = totalAnswers;
    }

    public Integer getCorrectAnswers() {
        return correctAnswers;
    }

    public void setCorrectAnswers(Integer correctAnswers) {
        this.correctAnswers = correctAnswers;
    }

    public Double getCorrectRate() {
        return correctRate;
    }

    public void setCorrectRate(Double correctRate) {
        this.correctRate = correctRate;
    }
}