package org.example.dto;

public class TeacherInfoDTO {
    private Long teacherId;
    private String nickname;

    // 构造器、getter和setter
    public TeacherInfoDTO(Long teacherId, String nickname) {
        this.teacherId = teacherId;
        this.nickname = nickname;
    }

    public Long getTeacherId() {
        return teacherId;
    }

    public void setTeacherId(Long teacherId) {
        this.teacherId = teacherId;
    }

    public String getNickname() {
        return nickname;
    }

    public void setNickname(String nickname) {
        this.nickname = nickname;
    }
}