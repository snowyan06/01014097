package org.example.service;

import org.example.dto.TeachingMaterialWithNicknameDTO;
import org.example.entity.TeachingMaterial;
import org.example.entity.User;
import org.example.exception.ResourceNotFoundException;
import org.example.repository.TeachingMaterialRepository;
import org.example.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class TeachingMaterialService {

    @Autowired
    private TeachingMaterialRepository repository;
    @Autowired
    private UserRepository userRepository;
    public List<TeachingMaterial> getAllMaterials() {
        return repository.findAll();
    }

    public TeachingMaterial getMaterialById(Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("教学资源未找到 ID: " + id));
    }

    public List<TeachingMaterial> getMaterialsByTeacherId(Long teacherId) {
        return repository.findByTeacherId(teacherId);
    }

    public TeachingMaterial createMaterial(TeachingMaterial material) {
        return repository.save(material);
    }

    public TeachingMaterial updateMaterial(Long id, TeachingMaterial updatedMaterial) {
        TeachingMaterial existing = getMaterialById(id);

        existing.setResourceName(updatedMaterial.getResourceName());
        existing.setFileType(updatedMaterial.getFileType());
        existing.setTeacherId(updatedMaterial.getTeacherId());
        existing.setFileSize(updatedMaterial.getFileSize());
        existing.setFilePath(updatedMaterial.getFilePath());

        return repository.save(existing);
    }

    public void deleteMaterial(Long id) {
        if (!repository.existsById(id)) {
            throw new ResourceNotFoundException("教学资源未找到 ID: " + id);
        }
        repository.deleteById(id);
    }

    // 新增方法：获取单个教学资料及其教师昵称
    public TeachingMaterialWithNicknameDTO getMaterialWithNickname(Long id) {
        TeachingMaterial material = getMaterialById(id);
        User teacher = userRepository.findById(material.getTeacherId())
                .orElseThrow(() -> new ResourceNotFoundException("未找到ID为 " + material.getTeacherId() + " 的用户"));

        return new TeachingMaterialWithNicknameDTO(material, teacher.getNickname());
    }

    // 新增方法：获取所有教学资料及其教师昵称
    public List<TeachingMaterialWithNicknameDTO> getAllMaterialsWithNickname() {
        return repository.findAll().stream()
                .map(material -> {
                    User teacher = userRepository.findById(material.getTeacherId())
                            .orElse(new User()); // 如果找不到用户，返回空User对象
                    return new TeachingMaterialWithNicknameDTO(material,
                            teacher.getNickname() != null ? teacher.getNickname() : "未知");
                })
                .collect(Collectors.toList());
    }

    // 新增方法：根据教师ID获取教学资料及其昵称
    public List<TeachingMaterialWithNicknameDTO> getMaterialsByTeacherIdWithNickname(Long teacherId) {
        User teacher = userRepository.findById(teacherId)
                .orElseThrow(() -> new ResourceNotFoundException("未找到ID为 " + teacherId + " 的用户"));

        return repository.findByTeacherId(teacherId).stream()
                .map(material -> new TeachingMaterialWithNicknameDTO(material, teacher.getNickname()))
                .collect(Collectors.toList());
    }
}