package poli.meets.authservice.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import javax.persistence.*;


@Entity
@Table(name = "user_role")
@Data
public class UserRole {

    @Id
    @GeneratedValue(strategy =  GenerationType.SEQUENCE, generator = "userRoleSequenceGenerator")
    @SequenceGenerator(
            name = "userRoleSequenceGenerator",
            sequenceName = "user_role_sequence_generator",
            allocationSize = 1
    )
    @Column(name = "id")
    private Long id;

    @JoinColumn(name = "user_id")
    @ManyToOne
    private User user;

    @JoinColumn(name = "role_id")
    @ManyToOne
    private Role role;
}
