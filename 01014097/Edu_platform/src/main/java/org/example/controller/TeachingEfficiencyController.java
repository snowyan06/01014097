package org.example.controller;


import org.example.dto.TeacherInfoDTO;
import org.example.entity.TeachingEfficiency;
import org.example.service.TeachingEfficiencyService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/teaching-efficiency")
public class TeachingEfficiencyController {

    private final TeachingEfficiencyService efficiencyService;

    @Autowired
    public TeachingEfficiencyController(TeachingEfficiencyService efficiencyService) {
        this.efficiencyService = efficiencyService;
    }

    @PostMapping("/record")
    public ResponseEntity<TeachingEfficiency> saveDailyRecord(
            @RequestParam("teacherId") Long teacherId,
            @RequestBody TeachingEfficiency record) {
        // 设置教师ID
        record.setTeacherId(teacherId);

        // 验证必要字段
        if (record.getDate() == null || record.getPrepTime() == null || record.getPrepRevisions() == null) {
            return ResponseEntity.badRequest().build();
        }

        TeachingEfficiency savedRecord = efficiencyService.saveOrUpdateDailyRecord(teacherId, record);
        return ResponseEntity.ok(savedRecord);
    }

    @GetMapping("/daily")
    public ResponseEntity<TeachingEfficiency> getDailyRecord(
            @RequestParam("teacherId") Long teacherId,
            @RequestParam("date") @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate date) {
        TeachingEfficiency record = efficiencyService.getDailyRecord(teacherId, date);
        return ResponseEntity.ok(record);
    }

    @GetMapping("/range")
    public ResponseEntity<List<TeachingEfficiency>> getRecordsInRange(
            @RequestParam("teacherId") Long teacherId,
            @RequestParam("startDate") @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam("endDate") @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate) {
        List<TeachingEfficiency> records = efficiencyService.getRecordsBetweenDates(teacherId, startDate, endDate);
        return ResponseEntity.ok(records);
    }

    @GetMapping("/index")
    public ResponseEntity<Map<String, Object>> calculateEfficiencyIndex(
            @RequestParam("teacherId") Long teacherId,
            @RequestParam("startDate") @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam("endDate") @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate) {
        Map<String, Object> indexData = efficiencyService.calculateEfficiencyIndex(teacherId, startDate, endDate);
        return ResponseEntity.ok(indexData);
    }

    @GetMapping("/teachers")
    public ResponseEntity<List<TeacherInfoDTO>> getAllTeachers() {
        List<TeacherInfoDTO> teachers = efficiencyService.getAllTeachers();
        return ResponseEntity.ok(teachers);
    }

    @GetMapping("/teachers-and-admins")
    public ResponseEntity<List<TeacherInfoDTO>> getAllTeachersAndAdmins() {
        List<TeacherInfoDTO> users = efficiencyService.getAllTeachersAndAdmins();
        return ResponseEntity.ok(users);
    }


}