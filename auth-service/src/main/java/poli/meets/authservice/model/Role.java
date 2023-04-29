package poli.meets.authservice.model;


import lombok.Data;

import javax.persistence.*;

@Entity
@Table(name = "role")
@Data
public class Role {

    @Id
    @GeneratedValue(strategy =  GenerationType.SEQUENCE, generator = "roleSequenceGenerator")
    @SequenceGenerator(
            name = "roleSequenceGenerator",
            sequenceName = "role_sequence_generator",
            allocationSize = 1
    )
    @Column(name = "id")
    private Long id;

    @Column(name = "name")
    private String name;

}
