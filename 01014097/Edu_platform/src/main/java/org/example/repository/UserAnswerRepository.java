// src/main/java/org/example/repository/UserAnswerRepository.java
package org.example.repository;

import org.example.dto.UserAnswerStatsDto;
import org.example.dto.UserAnswerWithNicknameDto;
import org.example.entity.UserAnswer;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface UserAnswerRepository extends JpaRepository<UserAnswer, Integer> {
    List<UserAnswer> findBySessionId(String sessionId);
    List<UserAnswer> findByUserId(Long userId);
    List<UserAnswer> findByUserIdAndSessionId(Long userId, String sessionId);

    @Query("SELECT DISTINCT u.userId FROM UserAnswer u")
    List<String> findDistinctUserIds();

    @Query("SELECT u.userId as userId, COUNT(u) as count FROM UserAnswer u GROUP BY u.userId")
    List<UserAnswerStatsDto> countUserAnswersByUserId();

    // 新增的 JPQL 连接查询
    @Query("SELECT new org.example.dto.UserAnswerWithNicknameDto(" +
            "ua.id, ua.questionType, ua.questionContent, ua.difficulty, " +
            "ua.userAnswer, ua.correctAnswer, ua.explanation, ua.isCorrect, " +
            "ua.answeredAt, ua.sessionId, ua.userId, u.nickname) " +
            "FROM UserAnswer ua LEFT JOIN User u ON ua.userId = u.id")
    List<UserAnswerWithNicknameDto> findAllWithNickname();

    // 带条件的查询
    @Query("SELECT new org.example.dto.UserAnswerWithNicknameDto(" +
            "ua.id, ua.questionType, ua.questionContent, ua.difficulty, " +
            "ua.userAnswer, ua.correctAnswer, ua.explanation, ua.isCorrect, " +
            "ua.answeredAt, ua.sessionId, ua.userId, u.nickname) " +
            "FROM UserAnswer ua LEFT JOIN User u ON ua.userId = u.id " +
            "WHERE ua.userId = :userId")
    List<UserAnswerWithNicknameDto> findByUserIdWithNickname(@Param("userId") Long userId);

    // 带统计的查询
    @Query("SELECT new org.example.dto.UserAnswerStatsDto(" +
            "ua.userId, COUNT(ua), u.nickname) " +
            "FROM UserAnswer ua LEFT JOIN User u ON ua.userId = u.id " +
            "GROUP BY ua.userId, u.nickname")
    List<UserAnswerStatsDto> countUserAnswersByUserIdWithNickname();

    // 当日活跃用户统计
    @Query("SELECT new org.example.dto.UserAnswerStatsDto(" +
            "ua.userId, COUNT(ua), u.nickname) " +
            "FROM UserAnswer ua LEFT JOIN User u ON ua.userId = u.id " +
            "WHERE DATE(ua.answeredAt) = CURRENT_DATE " +
            "GROUP BY ua.userId, u.nickname " +
            "ORDER BY COUNT(ua) DESC")
    List<UserAnswerStatsDto> countDailyActiveUsers();

    // 本周活跃用户统计
    @Query("SELECT new org.example.dto.UserAnswerStatsDto(" +
            "ua.userId, COUNT(ua), u.nickname) " +
            "FROM UserAnswer ua LEFT JOIN User u ON ua.userId = u.id " +
            "WHERE YEARWEEK(ua.answeredAt, 1) = YEARWEEK(CURRENT_DATE, 1) " +
            "GROUP BY ua.userId, u.nickname " +
            "ORDER BY COUNT(ua) DESC")
    List<UserAnswerStatsDto> countWeeklyActiveUsers();

    // 总使用次数统计 (按用户)
    @Query("SELECT new org.example.dto.UserAnswerStatsDto(" +
            "ua.userId, COUNT(ua), u.nickname) " +
            "FROM UserAnswer ua LEFT JOIN User u ON ua.userId = u.id " +
            "GROUP BY ua.userId, u.nickname " +
            "ORDER BY COUNT(ua) DESC")
    List<UserAnswerStatsDto> countTotalUsageByUser();
    
    // 正确率趋势查询
    @Query("SELECT DATE(ua.answeredAt) as date, " +
            "COUNT(ua) as totalAnswers, " +
            "SUM(CASE WHEN ua.isCorrect = true THEN 1 ELSE 0 END) as correctAnswers, " +
            "SUM(CASE WHEN ua.isCorrect = true THEN 1 ELSE 0 END)/COUNT(ua)*100 as correctRate " +
            "FROM UserAnswer ua " +
            "WHERE ua.userId = :userId " +
            "GROUP BY DATE(ua.answeredAt) " +
            "ORDER BY DATE(ua.answeredAt)")
    List<Object[]> findDailyCorrectRateByUser(@Param("userId") Long userId);

    // 知识点掌握度查询
    @Query("SELECT ua.questionType, " +
            "COUNT(ua) as totalQuestions, " +
            "SUM(CASE WHEN ua.isCorrect = true THEN 1 ELSE 0 END) as correctAnswers, " +
            "SUM(CASE WHEN ua.isCorrect = true THEN 1 ELSE 0 END)/COUNT(ua)*100 as masteryRate " +
            "FROM UserAnswer ua " +
            "WHERE ua.userId = :userId " +
            "GROUP BY ua.questionType")
    List<Object[]> findKnowledgeMasteryByUser(@Param("userId") Long userId);

    // 高频错题查询
    @Query("SELECT ua.questionContent, ua.questionType, ua.difficulty, " +
            "COUNT(ua) as errorCount, " +
            "ua.correctAnswer, ua.explanation " +
            "FROM UserAnswer ua " +
            "WHERE ua.userId = :userId AND ua.isCorrect = false " +
            "GROUP BY ua.questionContent, ua.questionType, ua.difficulty, ua.correctAnswer, ua.explanation " +
            "ORDER BY COUNT(ua) DESC " +
            "LIMIT 10")
    List<Object[]> findTopErrorQuestionsByUser(@Param("userId") Long userId);
}