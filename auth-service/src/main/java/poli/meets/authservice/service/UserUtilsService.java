package poli.meets.authservice.service;

import lombok.AllArgsConstructor;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import poli.meets.authservice.model.Role;
import poli.meets.authservice.model.RoleEnum;
import poli.meets.authservice.model.User;
import poli.meets.authservice.model.UserRole;
import poli.meets.authservice.repository.RoleRepository;
import poli.meets.authservice.repository.UserRepository;
import poli.meets.authservice.repository.UserRoleRepository;
import poli.meets.authservice.security.JwtTokenUtil;
import poli.meets.authservice.security.dtos.LoginRequest;
import poli.meets.authservice.security.dtos.LoginResponse;
import poli.meets.authservice.service.dtos.*;

import java.util.stream.Collectors;

@Service
@AllArgsConstructor
public class UserUtilsService {

    private final UserRepository userRepository;

    private final PasswordEncoder passwordEncoder;

    private final JwtTokenUtil jwtTokenUtil;

    private final UserService userService;

    private final UserRoleRepository userRoleRepository;

    private final RoleRepository roleRepository;

    private final CoreClient coreClient;

    public LoginResponse login(LoginRequest loginRequest) {

        UserDetails userDetails = userService.loadUserByUsername(loginRequest.getUsername());
        String jwtToken = jwtTokenUtil.generateToken(userDetails);

        return new LoginResponse(jwtToken);
    }

    public User register(UserRegisterDTO userDTO, RoleEnum roleEnum) throws Exception {
        if (userRepository.findByUsername(userDTO.getUsername()).isPresent()) {
            throw new Exception("Username already exists");
        }

        User savedUser = new User();

        savedUser.setUsername(userDTO.getUsername());
        savedUser.setPassword(passwordEncoder.encode(userDTO.getPassword()));

        savedUser = userRepository.save(savedUser);

        UserRole userRole = new UserRole();
        userRole.setUser(savedUser);
        userRole.setRole(roleRepository.findRoleByName(roleEnum).stream()
                .findAny().orElseThrow(IllegalStateException::new));


        userRoleRepository.save(userRole);

        return savedUser;
    }


    public User registerCustomer(CustomerRegisterDTO userDTO) throws Exception {
        User user = register(userDTO, RoleEnum.ROLE_CUSTOMER);

        CustomerDTO customerDTO = new CustomerDTO();

        customerDTO.setEmail(userDTO.getUsername());
        customerDTO.setFirstName(userDTO.getFirstName());
        customerDTO.setLastName(userDTO.getLastName());

        coreClient.makePostRequest(customerDTO);
        return user;
    }

    public User registerVendor(VendorRegisterDTO userDTO) throws Exception {
        User user = register(userDTO, RoleEnum.ROLE_VENDOR);

        VendorDTO vendorDTO = new VendorDTO();

        vendorDTO.setEmail(userDTO.getUsername());
        vendorDTO.setCompanyName(userDTO.getCompanyName());
        vendorDTO.setCompanyAddress(userDTO.getCompanyAddress());
        vendorDTO.setBankAccount(userDTO.getBankAccount());

        coreClient.makePostRequest(vendorDTO);
        return user;
    }

    public UserDTO getCurrentUser(String token) {
        String username = jwtTokenUtil.extractUsername(token);

        UserDTO userDTO = new UserDTO();

        userDTO.setUsername(username);
        userDTO.setRoles(roleRepository.findRolesByUsername(username).stream()
                .map(Role::getName).collect(Collectors.toList()));

        return userDTO;
    }
}
