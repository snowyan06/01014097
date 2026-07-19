package org.example.entity;

import jakarta.persistence.*;
import java.time.LocalDate;

@Entity
@Table(name = "teaching_efficiency")
public class TeachingEfficiency {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "teacher_id", nullable = false)
    private Long teacherId;

    @Column(nullable = false)
    private LocalDate date;

    @Column(name = "prep_time")
    private Integer prepTime = 0;

    @Column(name = "prep_revisions")
    private Integer prepRevisions = 0;

    @Column(name = "optimization_notes", columnDefinition = "TEXT")
    private String optimizationNotes;

    // Getter和Setter方法
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Long getTeacherId() {
        return teacherId;
    }

    public void setTeacherId(Long teacherId) {
        this.teacherId = teacherId;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public Integer getPrepTime() {
        return prepTime;
    }

    public void setPrepTime(Integer prepTime) {
        this.prepTime = prepTime;
    }

    public Integer getPrepRevisions() {
        return prepRevisions;
    }

    public void setPrepRevisions(Integer prepRevisions) {
        this.prepRevisions = prepRevisions;
    }

    public String getOptimizationNotes() {
        return optimizationNotes;
    }

    public void setOptimizationNotes(String optimizationNotes) {
        this.optimizationNotes = optimizationNotes;
    }
}