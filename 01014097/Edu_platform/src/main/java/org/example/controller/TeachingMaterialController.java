package org.example.controller;

import org.example.dto.TeachingMaterialWithNicknameDTO;
import org.example.entity.TeachingMaterial;
import org.example.service.TeachingMaterialService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/teaching-materials")
public class TeachingMaterialController {

    @Autowired
    private TeachingMaterialService service;

    @GetMapping
    public List<TeachingMaterial> getAll() {
        return service.getAllMaterials();
    }

    @GetMapping("/{id}")
    public ResponseEntity<TeachingMaterial> getById(@PathVariable("id") Long id) {
        return ResponseEntity.ok(service.getMaterialById(id));
    }

    @GetMapping("/teacher/{teacherId}")
    public List<TeachingMaterial> getByTeacherId(@PathVariable("teacherId") Long teacherId) {
        return service.getMaterialsByTeacherId(teacherId);
    }

    @PostMapping
    public TeachingMaterial create(@RequestBody TeachingMaterial material) {
        return service.createMaterial(material);
    }

    @PutMapping("/{id}")
    public ResponseEntity<TeachingMaterial> update(@PathVariable("id") Long id, @RequestBody TeachingMaterial material) {
        material.setId(id);
        return ResponseEntity.ok(service.updateMaterial(id, material));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable("id") Long id) {
        service.deleteMaterial(id);
        return ResponseEntity.noContent().build();
    }

    // 新增接口：获取单个教学资料及其教师昵称
    @GetMapping("/{id}/with-nickname")
    public ResponseEntity<TeachingMaterialWithNicknameDTO> getByIdWithNickname(@PathVariable("id") Long id) {
        return ResponseEntity.ok(service.getMaterialWithNickname(id));
    }

    // 新增接口：获取所有教学资料及其教师昵称
    @GetMapping("/with-nickname")
    public List<TeachingMaterialWithNicknameDTO> getAllWithNickname() {
        return service.getAllMaterialsWithNickname();
    }

    // 新增接口：根据教师ID获取教学资料及其昵称
    @GetMapping("/teacher/{teacherId}/with-nickname")
    public List<TeachingMaterialWithNicknameDTO> getByTeacherIdWithNickname(
            @PathVariable("teacherId") Long teacherId) {
        return service.getMaterialsByTeacherIdWithNickname(teacherId);
    }

}