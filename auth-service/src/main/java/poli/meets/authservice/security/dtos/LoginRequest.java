package poli.meets.authservice.security.dtos;

import lombok.Data;

@Data
public class LoginRequest {
    private String username;

    private String password;
}
