package org.example.service;

import org.example.dto.*;
import org.example.entity.UserAnswer;
import org.example.repository.UserAnswerRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class UserAnswerService {
    @Autowired
    private UserAnswerRepository userAnswerRepository;

    public UserAnswer saveUserAnswer(UserAnswer userAnswer) {
        return userAnswerRepository.save(userAnswer);
    }

    public List<UserAnswer> getAllUserAnswers() {
        return userAnswerRepository.findAll();
    }

    public UserAnswer getUserAnswerById(Integer id) {
        return userAnswerRepository.findById(id).orElse(null);
    }
    public List<UserAnswer> getUserAnswersBySessionId(String sessionId) {
        return userAnswerRepository.findBySessionId(sessionId);
    }
    public void deleteUserAnswer(Integer id) {
        userAnswerRepository.deleteById(id);
    }

    public UserAnswer updateUserAnswer(Integer id, UserAnswer updatedAnswer) {
        return userAnswerRepository.findById(id)
                .map(answer -> {
                    answer.setQuestionType(updatedAnswer.getQuestionType());
                    answer.setQuestionContent(updatedAnswer.getQuestionContent());
                    answer.setDifficulty(updatedAnswer.getDifficulty());
                    answer.setUserAnswer(updatedAnswer.getUserAnswer());
                    answer.setCorrectAnswer(updatedAnswer.getCorrectAnswer());
                    answer.setExplanation(updatedAnswer.getExplanation());
                    answer.setIsCorrect(updatedAnswer.getIsCorrect());
                    answer.setSessionId(updatedAnswer.getSessionId());
                    return userAnswerRepository.save(answer);
                })
                .orElseGet(() -> {
                    updatedAnswer.setId(id);
                    return userAnswerRepository.save(updatedAnswer);
                });
    }

    public List<UserAnswer> getUserAnswersByUserId(Long userId) {
        return userAnswerRepository.findByUserId(userId);
    }

    public List<UserAnswer> getUserAnswersByUserIdAndSessionId(Long userId, String sessionId) {
        return userAnswerRepository.findByUserIdAndSessionId(userId, sessionId);
    }

    public List<String> getAllDistinctUserIds() {
        return userAnswerRepository.findDistinctUserIds();
    }

    public List<UserAnswerStatsDto> getUserAnswerStats() {
        return userAnswerRepository.countUserAnswersByUserId();
    }
    public List<UserAnswerWithNicknameDto> getUserAnswersWithNickname() {
        return userAnswerRepository.findAllWithNickname();
    }

    public List<UserAnswerWithNicknameDto> getUserAnswersByUserIdWithNickname(Long userId) {
        return userAnswerRepository.findByUserIdWithNickname(userId);
    }

    public List<UserAnswerStatsDto> getUserAnswerStatsWithNickname() {
        return userAnswerRepository.countUserAnswersByUserIdWithNickname();
    }

    public List<UserAnswerStatsDto> getDailyActiveUsers() {
        return userAnswerRepository.countDailyActiveUsers();
    }

    public List<UserAnswerStatsDto> getWeeklyActiveUsers() {
        return userAnswerRepository.countWeeklyActiveUsers();
    }

    public List<UserAnswerStatsDto> getTotalUsageByUser() {
        return userAnswerRepository.countTotalUsageByUser();
    }

    public UserAnswer partiallyUpdateUserAnswer(Integer id, Map<String, Object> updates) {
        return userAnswerRepository.findById(id)
                .map(answer -> {
                    // 遍历更新映射中的每个字段
                    updates.forEach((key, value) -> {
                        switch (key) {
                            case "questionType":
                                answer.setQuestionType((String) value);
                                break;
                            case "questionContent":
                                answer.setQuestionContent((String) value);
                                break;
                            case "difficulty":
                                answer.setDifficulty((String) value);
                                break;
                            case "userAnswer":
                                answer.setUserAnswer((String) value);
                                break;
                            case "correctAnswer":
                                answer.setCorrectAnswer((String) value);
                                break;
                            case "explanation":
                                answer.setExplanation((String) value);
                                break;
                            case "isCorrect":
                                answer.setIsCorrect((Boolean) value);
                                break;
                            case "sessionId":
                                answer.setSessionId((String) value);
                                break;
                            // answeredAt 通常不应该通过 API 更新
                        }
                    });
                    return userAnswerRepository.save(answer);
                })
                .orElseThrow(() -> new RuntimeException("UserAnswer not found with id: " + id));
    }
    // 在UserAnswerService.java中添加
    public List<CorrectRateTrendDto> getCorrectRateTrend(Long userId) {
        List<Object[]> results = userAnswerRepository.findDailyCorrectRateByUser(userId);
        return results.stream().map(r -> new CorrectRateTrendDto(
                LocalDate.parse(r[0].toString()),
                ((Number)r[1]).intValue(),
                ((Number)r[2]).intValue(),
                ((Number)r[3]).doubleValue()
        )).collect(Collectors.toList());
    }

    // 在UserAnswerService.java中添加
    public List<KnowledgeMasteryDto> getKnowledgeMastery(Long userId) {
        List<Object[]> results = userAnswerRepository.findKnowledgeMasteryByUser(userId);
        return results.stream().map(r -> new KnowledgeMasteryDto(
                (String)r[0],
                ((Number)r[1]).intValue(),
                ((Number)r[2]).intValue(),
                ((Number)r[3]).doubleValue()
        )).collect(Collectors.toList());
    }

    // 在UserAnswerService.java中添加
    public List<FrequentErrorDto> getFrequentErrors(Long userId) {
        List<Object[]> results = userAnswerRepository.findTopErrorQuestionsByUser(userId);
        return results.stream().map(r -> new FrequentErrorDto(
                (String)r[0],
                (String)r[1],
                (String)r[2],
                ((Number)r[3]).intValue(),
                (String)r[4],
                (String)r[5]
        )).collect(Collectors.toList());
    }

}