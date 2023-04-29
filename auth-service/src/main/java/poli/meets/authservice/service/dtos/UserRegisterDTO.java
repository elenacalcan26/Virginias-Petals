package poli.meets.authservice.service.dtos;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class UserRegisterDTO {

    private String username;

    private String password;
}
