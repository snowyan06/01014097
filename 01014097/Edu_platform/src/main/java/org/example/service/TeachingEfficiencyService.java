package org.example.service;

import org.example.dto.TeacherInfoDTO;
import org.example.entity.TeachingEfficiency;
import org.example.entity.User;
import org.example.exception.ResourceNotFoundException;
import org.example.repository.TeachingEfficiencyRepository;
import org.example.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class TeachingEfficiencyService {

    private final TeachingEfficiencyRepository repository;
    private final UserRepository userRepository;
    @Autowired
    public TeachingEfficiencyService(TeachingEfficiencyRepository repository, UserRepository userRepository) {
        this.repository = repository;
        this.userRepository = userRepository;
    }
    public List<TeacherInfoDTO> getAllTeachers() {
        List<User> teachers = userRepository.findByRole("teacher");
        return teachers.stream()
                .map(user -> new TeacherInfoDTO(user.getId(), user.getNickname()))
                .collect(Collectors.toList());
    }
    public List<TeacherInfoDTO> getAllTeachersAndAdmins() {
        // 调用新的方法，查询 teacher 和 admin
        List<User> users = userRepository.findTeachersAndAdmins();

        return users.stream()
                .map(user -> new TeacherInfoDTO(user.getId(), user.getNickname()))
                .collect(Collectors.toList());
    }

    // 保存或更新每日记录
    public TeachingEfficiency saveOrUpdateDailyRecord(Long teacherId, TeachingEfficiency record) {
        // 设置教师ID
        record.setTeacherId(teacherId);

        // 检查是否已有当日记录
        Optional<TeachingEfficiency> existing = repository.findByTeacherIdAndDate(teacherId, record.getDate());

        if (existing.isPresent()) {
            // 更新现有记录
            TeachingEfficiency existingRecord = existing.get();
            existingRecord.setPrepTime(record.getPrepTime());
            existingRecord.setPrepRevisions(record.getPrepRevisions());
            existingRecord.setOptimizationNotes(record.getOptimizationNotes());
            return repository.save(existingRecord);
        } else {
            // 创建新记录
            return repository.save(record);
        }
    }

    // 获取每日记录
    public TeachingEfficiency getDailyRecord(Long teacherId, LocalDate date) {
        return repository.findByTeacherIdAndDate(teacherId, date)
                .orElseThrow(() -> new ResourceNotFoundException("Record not found for date: " + date));
    }

    // 获取日期范围内的记录
    public List<TeachingEfficiency> getRecordsBetweenDates(Long teacherId, LocalDate startDate, LocalDate endDate) {
        return repository.findByTeacherIdAndDateBetween(teacherId, startDate, endDate);
    }

    // 计算效率指数
    public Map<String, Object> calculateEfficiencyIndex(Long teacherId, LocalDate startDate, LocalDate endDate) {
        // 获取统计数据
        Double avgPrepTime = repository.findAveragePrepTime(teacherId, startDate, endDate);
        Double avgPrepRevisions = repository.findAveragePrepRevisions(teacherId, startDate, endDate);

        Long optimizationCount = repository.countOptimizationNotes(teacherId, startDate, endDate);

        // 处理可能的null值
        avgPrepTime = avgPrepTime != null ? avgPrepTime : 0.0;
        avgPrepRevisions = avgPrepRevisions != null ? avgPrepRevisions : 0.0;


        // 计算效率指数 (可根据需求调整公式)
        double efficiencyIndex = (avgPrepTime * 0.6) + (avgPrepRevisions * 0.4);


        // 构建返回结果
        Map<String, Object> result = new HashMap<>();
        result.put("efficiencyIndex", Math.round(efficiencyIndex * 100) / 100.0);
        result.put("avgPrepTime", Math.round(avgPrepTime * 100) / 100.0);
        result.put("avgPrepRevisions", Math.round(avgPrepRevisions * 100) / 100.0);
        result.put("optimizationCount", optimizationCount);
        result.put("startDate", startDate);
        result.put("endDate", endDate);

        return result;
    }

}