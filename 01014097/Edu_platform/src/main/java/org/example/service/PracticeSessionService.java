package org.example.service;

import org.example.entity.PracticeSession;
import org.example.repository.PracticeSessionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.math.BigDecimal;
import java.util.List;

@Service
public class PracticeSessionService {
    @Autowired
    private PracticeSessionRepository repository;

    public PracticeSession createSession(PracticeSession session) {
        // 计算正确率
        if (session.getTotalQuestions() != null && session.getTotalQuestions() > 0) {
            BigDecimal accuracy = BigDecimal.valueOf(session.getCorrectCount())
                    .divide(BigDecimal.valueOf(session.getTotalQuestions()), 4, BigDecimal.ROUND_HALF_UP)
                    .multiply(BigDecimal.valueOf(100));
            session.setAccuracyRate(accuracy);
        }
        return repository.save(session);
    }

    public List<PracticeSession> getAllSessions() {
        return repository.findAll();
    }

    public PracticeSession getSessionById(Integer id) {
        return repository.findById(id).orElse(null);
    }

    public PracticeSession getSessionBySessionId(String sessionId) {
        return repository.findBySessionId(sessionId);
    }

    // 新增按userId查询的方法
    public List<PracticeSession> getSessionsByUserId(Integer userId) {
        return repository.findByUserId(userId);
    }

    public PracticeSession updateSession(Integer id, PracticeSession updatedSession) {
        return repository.findById(id)
                .map(session -> {
                    session.setUserId(updatedSession.getUserId());  // 更新userId
                    session.setTitle(updatedSession.getTitle());
                    session.setTotalQuestions(updatedSession.getTotalQuestions());
                    session.setCorrectCount(updatedSession.getCorrectCount());
                    session.setScore(updatedSession.getScore());
                    session.setSessionId(updatedSession.getSessionId());

                    // 重新计算正确率
                    if (updatedSession.getTotalQuestions() != null && updatedSession.getTotalQuestions() > 0) {
                        BigDecimal accuracy = BigDecimal.valueOf(updatedSession.getCorrectCount())
                                .divide(BigDecimal.valueOf(updatedSession.getTotalQuestions()), 4, BigDecimal.ROUND_HALF_UP)
                                .multiply(BigDecimal.valueOf(100));
                        session.setAccuracyRate(accuracy);
                    }

                    return repository.save(session);
                })
                .orElseGet(() -> {
                    updatedSession.setId(id);
                    return repository.save(updatedSession);
                });
    }

    public void deleteSession(Integer id) {
        repository.deleteById(id);
    }
}