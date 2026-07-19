package org.example.controller;

import org.example.entity.PracticeSession;
import org.example.service.PracticeSessionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/practice-sessions")
public class PracticeSessionController {
    @Autowired
    private PracticeSessionService sessionService;

    @PostMapping
    public PracticeSession createSession(@RequestBody PracticeSession session) {
        return sessionService.createSession(session);
    }

    @GetMapping
    public List<PracticeSession> getAllSessions() {
        return sessionService.getAllSessions();
    }

    @GetMapping("/{id}")
    public PracticeSession getSessionById(@PathVariable("id") Integer id) {
        return sessionService.getSessionById(id);
    }

    @GetMapping("/by-session/{sessionId}")
    public PracticeSession getSessionBySessionId(@PathVariable("sessionId") String sessionId) {
        return sessionService.getSessionBySessionId(sessionId);
    }

    // 新增按userId查询的接口
    @GetMapping("/by-user/{userId}")
    public List<PracticeSession> getSessionsByUserId(@PathVariable("userId") Integer userId) {
        return sessionService.getSessionsByUserId(userId);
    }

    @PutMapping("/{id}")
    public PracticeSession updateSession(
            @PathVariable("id") Integer id,
            @RequestBody PracticeSession session) {
        return sessionService.updateSession(id, session);
    }

    @DeleteMapping("/{id}")
    public void deleteSession(@PathVariable("id") Integer id) {
        sessionService.deleteSession(id);
    }
}