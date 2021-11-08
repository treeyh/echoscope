
/*==============================================================*/
/* Table: tb_class                                              */
/*==============================================================*/
create table tb_class (
   id                   SERIAL not null,
   name                 varchar(16)          not null default '',
   code                 varchar(16)          not null default '',
   grade                INT4                 not null default 1,
   class_teacher        varchar(16)          not null default '',
   remark               varchar(512)         not null default '',
   status               INT4                 not null default 1,
   creator              bigint               not null default '0',
   create_time          TIMESTAMP WITH TIME ZONE not null default CURRENT_TIMESTAMP,
   updator              bigint               not null default '0',
   update_time          TIMESTAMP WITH TIME ZONE not null default CURRENT_TIMESTAMP,
   version              int                  not null default '1',
   del_flag             INT2                 not null default 2,
   constraint PK_TB_CLASS primary key (id)
);

comment on table tb_class is
'班级';

comment on column tb_class.id is
'id主键';

comment on column tb_class.name is
'名称';

comment on column tb_class.code is
'编号';

comment on column tb_class.grade is
'年级';

comment on column tb_class.class_teacher is
'班主任';

comment on column tb_class.remark is
'备注';

comment on column tb_class.status is
'状态，1可用，2不可用';

comment on column tb_class.creator is
'创建人';

comment on column tb_class.create_time is
'创建时间';

comment on column tb_class.updator is
'更新人';

comment on column tb_class.update_time is
'更新时间';

comment on column tb_class.version is
'乐观锁版本号';

comment on column tb_class.del_flag is
'是否删除，1删除，2未删除';

/*==============================================================*/
/* Index: idx_tb_class_code                                     */
/*==============================================================*/
create  index idx_tb_class_code on tb_class (
code
);

/*==============================================================*/
/* Index: idx_tb_class_name                                     */
/*==============================================================*/
create  index idx_tb_class_name on tb_class (
name
);

/*==============================================================*/
/* Index: idx_tb_class_create_time                              */
/*==============================================================*/
create  index idx_tb_class_create_time on tb_class (
create_time
);

/*==============================================================*/
/* Table: tb_class_student                                      */
/*==============================================================*/
create table tb_class_student (
   id                   SERIAL not null,
   student_id           bigint               not null default '0',
   class_id             bigint               not null default '0',
   sort                 int                  not null default '0',
   status               INT4                 not null default 1,
   creator              bigint               not null default '0',
   create_time          TIMESTAMP WITH TIME ZONE not null default CURRENT_TIMESTAMP,
   updator              bigint               not null default '0',
   update_time          TIMESTAMP WITH TIME ZONE not null default CURRENT_TIMESTAMP,
   version              int                  not null default '1',
   del_flag             INT2                 not null default 2,
   constraint PK_TB_CLASS_STUDENT primary key (id)
);

comment on table tb_class_student is
'班级学生';

comment on column tb_class_student.id is
'id主键';

comment on column tb_class_student.student_id is
'学生id';

comment on column tb_class_student.class_id is
'班级id';

comment on column tb_class_student.sort is
'排序';

comment on column tb_class_student.status is
'状态，1可用，2不可用';

comment on column tb_class_student.creator is
'创建人';

comment on column tb_class_student.create_time is
'创建时间';

comment on column tb_class_student.updator is
'更新人';

comment on column tb_class_student.update_time is
'更新时间';

comment on column tb_class_student.version is
'乐观锁版本号';

comment on column tb_class_student.del_flag is
'是否删除，1删除，2未删除';

/*==============================================================*/
/* Index: idx_student_code                                      */
/*==============================================================*/
create  index idx_student_code on tb_class_student (
class_id
);

/*==============================================================*/
/* Index: idx_student_name                                      */
/*==============================================================*/
create  index idx_student_name on tb_class_student (
student_id
);

/*==============================================================*/
/* Index: idx_student_create_time                               */
/*==============================================================*/
create  index idx_student_create_time on tb_class_student (
create_time
);

/*==============================================================*/
/* Table: tb_student                                            */
/*==============================================================*/
create table tb_student (
   id                   SERIAL not null,
   name                 varchar(16)          not null default '',
   name_en              varchar(256)         not null default '',
   code                 varchar(32)          not null default '',
   sex                  INT4                 not null default 0,
   mobile               varchar(16)          not null default '',
   address              varchar(128)         not null default '',
   remark               varchar(512)         not null default '',
   status               INT4                 not null default 1,
   creator              bigint               not null default '0',
   create_time          TIMESTAMP WITH TIME ZONE not null default CURRENT_TIMESTAMP,
   updator              bigint               not null default '0',
   update_time          TIMESTAMP WITH TIME ZONE not null default CURRENT_TIMESTAMP,
   version              int                  not null default '1',
   del_flag             INT2                 not null default 2,
   constraint PK_TB_STUDENT primary key (id)
);

comment on table tb_student is
'学生';

comment on column tb_student.id is
'id主键';

comment on column tb_student.name is
'姓名';

comment on column tb_student.name_en is
'英文姓名';

comment on column tb_student.code is
'学号';

comment on column tb_student.sex is
'性别，1：男，2：女，0：未知';

comment on column tb_student.mobile is
'电话';

comment on column tb_student.address is
'地址';

comment on column tb_student.remark is
'备注';

comment on column tb_student.status is
'状态，1在校，2毕业，3休学';

comment on column tb_student.creator is
'创建人';

comment on column tb_student.create_time is
'创建时间';

comment on column tb_student.updator is
'更新人';

comment on column tb_student.update_time is
'更新时间';

comment on column tb_student.version is
'乐观锁版本号';

comment on column tb_student.del_flag is
'是否删除，1删除，2未删除';

/*==============================================================*/
/* Index: idx_tb_student_code                                   */
/*==============================================================*/
create  index idx_tb_student_code on tb_student (
code
);

/*==============================================================*/
/* Index: idx_tb_student_name                                   */
/*==============================================================*/
create  index idx_tb_student_name on tb_student (
name
);

/*==============================================================*/
/* Index: idx_tb_student_create_time                            */
/*==============================================================*/
create  index idx_tb_student_create_time on tb_student (
create_time
);
