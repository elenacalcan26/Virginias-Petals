package poli.meets.authservice.service;

import lombok.AllArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import poli.meets.authservice.model.User;
import poli.meets.authservice.repository.UserRepository;
import poli.meets.authservice.security.JwtTokenUtil;
import poli.meets.authservice.security.dtos.LoginRequest;
import poli.meets.authservice.security.dtos.LoginResponse;
import poli.meets.authservice.service.dtos.UserRegisterDTO;

import java.util.Optional;

@Service
@AllArgsConstructor
public class UserUtilsService {

    private final UserRepository userRepository;

    private final PasswordEncoder passwordEncoder;

    private final JwtTokenUtil jwtTokenUtil;

    private final UserService userService;

    public LoginResponse login(LoginRequest loginRequest) {

        UserDetails userDetails = userService.loadUserByUsername(loginRequest.getUsername());
        String jwtToken = jwtTokenUtil.generateToken(userDetails);

        return new LoginResponse(jwtToken);
    }


    public User register(UserRegisterDTO userDTO) throws Exception {
        if (userRepository.findByUsername(userDTO.getUsername()).isPresent()) {
            throw new Exception("Username already exists");
        }

        User savedUser = new User();

        savedUser.setUsername(userDTO.getUsername());
        savedUser.setPassword(passwordEncoder.encode(userDTO.getPassword()));

        userRepository.save(savedUser);


        return savedUser;
    }
}
