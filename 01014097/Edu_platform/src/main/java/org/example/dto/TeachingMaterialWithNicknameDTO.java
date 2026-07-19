package org.example.dto;

import org.example.entity.TeachingMaterial;

public class TeachingMaterialWithNicknameDTO {
    private TeachingMaterial material;  // 教学资料信息
    private String teacherNickname;    // 教师昵称

    // 构造方法
    public TeachingMaterialWithNicknameDTO(TeachingMaterial material, String teacherNickname) {
        this.material = material;
        this.teacherNickname = teacherNickname;
    }

    // getter 和 setter
    public TeachingMaterial getMaterial() {
        return material;
    }

    public void setMaterial(TeachingMaterial material) {
        this.material = material;
    }

    public String getTeacherNickname() {
        return teacherNickname;
    }

    public void setTeacherNickname(String teacherNickname) {
        this.teacherNickname = teacherNickname;
    }
}