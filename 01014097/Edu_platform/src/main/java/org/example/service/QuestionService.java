package org.example.service;

import org.example.dto.TeacherActivityDTO;
import org.example.entity.Question;
import org.example.exception.ResourceNotFoundException;
import org.example.repository.QuestionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@Transactional
public class QuestionService {
    @Autowired
    private QuestionRepository questionRepository;

    public Question createQuestion(Question question) {
        if (questionRepository.existsByQuestionId(question.getQuestionId())) {
            throw new IllegalArgumentException("Question ID already exists");
        }
        return questionRepository.save(question);
    }

    public List<Question> getAllQuestions() {
        return questionRepository.findAll();
    }

    public Question getQuestionById(Long id) {
        return questionRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Question not found with id: " + id));
    }

    public Question getByQuestionId(String questionId) {
        return questionRepository.findByQuestionId(questionId)
                .orElseThrow(() -> new ResourceNotFoundException("Question not found with ID: " + questionId));
    }

    public Question updateQuestion(Long id, Question questionDetails) {
        Question question = getQuestionById(id);
        question.setQuestionId(questionDetails.getQuestionId());
        question.setType(questionDetails.getType());
        question.setContent(questionDetails.getContent());
        question.setAnswer(questionDetails.getAnswer());
        question.setDifficulty(questionDetails.getDifficulty());
        question.setSource(questionDetails.getSource());
        return questionRepository.save(question);
    }

    public void deleteQuestion(Long id) {
        Question question = getQuestionById(id);
        questionRepository.delete(question);
    }

    public List<TeacherActivityDTO> getDailyTeacherActivity() {
        return new ArrayList<>();
    }

    public List<TeacherActivityDTO> getWeeklyTeacherActivity() {
        return new ArrayList<>();
    }

    // QuestionService.java
    public List<TeacherActivityDTO> getTotalTeacherActivity() {
        return new ArrayList<>();
    }

}