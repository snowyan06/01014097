package org.example.dto;

import lombok.Data;
import lombok.AllArgsConstructor;

@Data
@AllArgsConstructor
public class TeacherActivityDTO {
    private Long teacherId;
    private String nickname;
    private Long questionCount;
}