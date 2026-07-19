package org.example.repository;

import org.example.entity.TeachingMaterial;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TeachingMaterialRepository extends JpaRepository<TeachingMaterial, Long> {
    List<TeachingMaterial> findByTeacherId(Long teacherId);
}