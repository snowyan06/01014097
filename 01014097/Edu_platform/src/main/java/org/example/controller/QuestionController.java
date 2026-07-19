package org.example.controller;

import org.example.dto.TeacherActivityDTO;
import org.example.entity.Question;
import org.example.service.QuestionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/questions")
public class QuestionController {
    @Autowired
    private QuestionService questionService;

    @PostMapping
    public ResponseEntity<Question> createQuestion(@RequestBody Question question) {
        return ResponseEntity.status(HttpStatus.CREATED).body(questionService.createQuestion(question));
    }

    @GetMapping
    public ResponseEntity<List<Question>> getAllQuestions() {
        return ResponseEntity.ok(questionService.getAllQuestions());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Question> getQuestionById(
            @PathVariable("id") Long id) {  // 明确指定参数名
        return ResponseEntity.ok(questionService.getQuestionById(id));
    }

    @GetMapping("/by-number/{questionId}")
    public ResponseEntity<Question> getByQuestionId(
            @PathVariable("questionId") String questionId) {  // 明确指定参数名
        return ResponseEntity.ok(questionService.getByQuestionId(questionId));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Question> updateQuestion(
            @PathVariable("id") Long id,  // 明确指定参数名
            @RequestBody Question questionDetails) {
        return ResponseEntity.ok(questionService.updateQuestion(id, questionDetails));
    }

    // 删除题目（修正）
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteQuestion(
            @PathVariable("id") Long id) {  // 明确指定参数名
        questionService.deleteQuestion(id);
        return ResponseEntity.noContent().build();
    }
    @GetMapping("/daily")
    public ResponseEntity<List<TeacherActivityDTO>> getDailyTeacherActivity() {
        return ResponseEntity.ok(questionService.getDailyTeacherActivity());
    }

    @GetMapping("/weekly")
    public ResponseEntity<List<TeacherActivityDTO>> getWeeklyTeacherActivity() {
        return ResponseEntity.ok(questionService.getWeeklyTeacherActivity());
    }

    @GetMapping("/total")
    public ResponseEntity<List<TeacherActivityDTO>> getTotalTeacherActivity() {
        return ResponseEntity.ok(questionService.getTotalTeacherActivity());
    }
}