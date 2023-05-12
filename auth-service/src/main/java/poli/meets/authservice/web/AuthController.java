package poli.meets.authservice.web;

import lombok.AllArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.web.bind.annotation.*;
import poli.meets.authservice.model.User;
import poli.meets.authservice.security.dtos.LoginRequest;
import poli.meets.authservice.service.UserUtilsService;
import poli.meets.authservice.service.dtos.CustomerRegisterDTO;
import poli.meets.authservice.service.dtos.UserDTO;;
import poli.meets.authservice.service.dtos.VendorRegisterDTO;

@RestController
@RequestMapping("/api")
@AllArgsConstructor
public class AuthController {

    private final AuthenticationManager authenticationManager;

    private final UserUtilsService userUtilsService;

    @PostMapping("/login")
    public ResponseEntity<?> authenticateUser(@RequestBody LoginRequest loginRequest) {
        try {
            authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(loginRequest.getUsername(), loginRequest.getPassword()));
        } catch (BadCredentialsException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Invalid credentials");
        }

        return ResponseEntity.ok(userUtilsService.login(loginRequest));
    }

    @PostMapping("/register-customer")
    public ResponseEntity<?> registerCustomer(@RequestBody CustomerRegisterDTO user) {
        try {
            User savedUser = userUtilsService.registerCustomer(user);
            return ResponseEntity.ok(savedUser);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(e.getMessage());
        }
    }

    @PostMapping("/register-vendor")
    public ResponseEntity<?> registerVendor(@RequestBody VendorRegisterDTO user) {
        try {
            User savedUser = userUtilsService.registerVendor(user);
            return ResponseEntity.ok(savedUser);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(e.getMessage());
        }
    }

    @GetMapping("/current-user")
    public ResponseEntity<UserDTO> getCurrentUser(@RequestHeader("Authorization") String token) {
        return ResponseEntity.ok(userUtilsService.getCurrentUser(token.substring(7)));
    }

}