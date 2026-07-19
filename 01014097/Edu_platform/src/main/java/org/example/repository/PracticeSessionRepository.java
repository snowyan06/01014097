package org.example.repository;

import org.example.entity.PracticeSession;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface PracticeSessionRepository extends JpaRepository<PracticeSession, Integer> {
    PracticeSession findBySessionId(String sessionId);

    // 新增按userId查询的方法
    List<PracticeSession> findByUserId(Integer userId);
}