package org.example.repository;

import org.example.entity.TeachingEfficiency;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Repository
public interface TeachingEfficiencyRepository extends JpaRepository<TeachingEfficiency, Long> {

    // 根据教师ID和日期查找记录
    Optional<TeachingEfficiency> findByTeacherIdAndDate(Long teacherId, LocalDate date);

    // 查找指定日期范围内的记录
    List<TeachingEfficiency> findByTeacherIdAndDateBetween(Long teacherId, LocalDate startDate, LocalDate endDate);

    // 计算平均备课时间
    @Query("SELECT AVG(te.prepTime) FROM TeachingEfficiency te WHERE te.teacherId = ?1 AND te.date BETWEEN ?2 AND ?3")
    Double findAveragePrepTime(Long teacherId, LocalDate startDate, LocalDate endDate);

    // 计算平均备课修改次数
    @Query("SELECT AVG(te.prepRevisions) FROM TeachingEfficiency te WHERE te.teacherId = ?1 AND te.date BETWEEN ?2 AND ?3")
    Double findAveragePrepRevisions(Long teacherId, LocalDate startDate, LocalDate endDate);


    // 计算优化建议数量
    @Query("SELECT COUNT(te) FROM TeachingEfficiency te WHERE te.teacherId = ?1 AND te.date BETWEEN ?2 AND ?3 AND te.optimizationNotes IS NOT NULL AND te.optimizationNotes <> ''")
    Long countOptimizationNotes(Long teacherId, LocalDate startDate, LocalDate endDate);



}