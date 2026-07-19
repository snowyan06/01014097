package org.example.controller;
import org.example.dto.*;
import org.example.entity.UserAnswer;
import org.example.service.UserAnswerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/user-answers")
public class UserAnswerController {
    @Autowired
    private UserAnswerService userAnswerService;

    @PostMapping
    public UserAnswer createUserAnswer(@RequestBody UserAnswer userAnswer) {
        return userAnswerService.saveUserAnswer(userAnswer);
    }

    @GetMapping
    public List<UserAnswer> getAllUserAnswers() {
        return userAnswerService.getAllUserAnswers();
    }

    @GetMapping("/{id}")
    public UserAnswer getUserAnswerById(@PathVariable("id") Integer id) {
        return userAnswerService.getUserAnswerById(id);
    }
    @GetMapping("/by-session/{sessionId}")
    public List<UserAnswer> getUserAnswersBySessionId(@PathVariable("sessionId") String sessionId) {
        return userAnswerService.getUserAnswersBySessionId(sessionId);
    }

    @PutMapping("/{id}")
    public UserAnswer updateUserAnswer(@PathVariable("id") Integer id, @RequestBody UserAnswer userAnswer) {
        return userAnswerService.updateUserAnswer(id, userAnswer);
    }

    @DeleteMapping("/{id}")
    public void deleteUserAnswer(@PathVariable("id") Integer id) {
        userAnswerService.deleteUserAnswer(id);
    }

    @PatchMapping("/{id}")
    public UserAnswer partiallyUpdateUserAnswer(
            @PathVariable("id") Integer id,
            @RequestBody Map<String, Object> updates) {
        return userAnswerService.partiallyUpdateUserAnswer(id, updates);
    }

    // 新增按用户ID查询的端点
    @GetMapping("/user/{userId}")
    public List<UserAnswer> getUserAnswersByUserId(@PathVariable("userId") Long userId) {
        return userAnswerService.getUserAnswersByUserId(userId);
    }

    // 可选：按用户ID和sessionId联合查询的端点
    @GetMapping("/user/{userId}/session/{sessionId}")
    public List<UserAnswer> getUserAnswersByUserIdAndSessionId(
            @PathVariable("userId") Long userId,
            @PathVariable("sessionId") String sessionId) {
        return userAnswerService.getUserAnswersByUserIdAndSessionId(userId, sessionId);
    }
    @GetMapping("/distinct-user-ids")
    public List<String> getAllDistinctUserIds() {
        return userAnswerService.getAllDistinctUserIds();
    }

    @GetMapping("/user-stats")
    public List<UserAnswerStatsDto> getUserAnswerStats() {
        return userAnswerService.getUserAnswerStats();
    }
    @GetMapping("/with-nickname")
    public List<UserAnswerWithNicknameDto> getUserAnswersWithNickname() {
        return userAnswerService.getUserAnswersWithNickname();
    }

    @GetMapping("/user/{userId}/with-nickname")
    public List<UserAnswerWithNicknameDto> getUserAnswersByUserIdWithNickname(
            @PathVariable("userId") Long userId) {
        return userAnswerService.getUserAnswersByUserIdWithNickname(userId);
    }

    @GetMapping("/user-stats-with-nickname")
    public List<UserAnswerStatsDto> getUserAnswerStatsWithNickname() {
        return userAnswerService.getUserAnswerStatsWithNickname();
    }

    @GetMapping("/stats/daily-active")
    public List<UserAnswerStatsDto> getDailyActiveUsers() {
        return userAnswerService.getDailyActiveUsers();
    }

    @GetMapping("/stats/weekly-active")
    public List<UserAnswerStatsDto> getWeeklyActiveUsers() {
        return userAnswerService.getWeeklyActiveUsers();
    }

    @GetMapping("/stats/total-usage")
    public List<UserAnswerStatsDto> getTotalUsageByUser() {
        return userAnswerService.getTotalUsageByUser();
    }
    // 在UserAnswerController.java中添加
    @GetMapping("/stats/correct-rate-trend/{userId}")
    public List<CorrectRateTrendDto> getCorrectRateTrend(@PathVariable("userId") Long userId) {
        return userAnswerService.getCorrectRateTrend(userId);
    }

    // 在UserAnswerController.java中添加
    @GetMapping("/stats/knowledge-mastery/{userId}")
    public List<KnowledgeMasteryDto> getKnowledgeMastery(@PathVariable("userId") Long userId) {
        return userAnswerService.getKnowledgeMastery(userId);
    }

    // 在UserAnswerController.java中添加
    @GetMapping("/stats/frequent-errors/{userId}")
    public List<FrequentErrorDto> getFrequentErrors(@PathVariable("userId") Long userId) {
        return userAnswerService.getFrequentErrors(userId);
    }
}