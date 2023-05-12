package poli.meets.authservice.service.dtos;

import lombok.Data;
import poli.meets.authservice.model.RoleEnum;

import java.util.List;

@Data
public class UserDTO {

    private String username;

    private List<RoleEnum> roles;
}
