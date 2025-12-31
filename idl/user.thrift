/**
 * 用户服务 IDL 定义
 * User Service Interface Definition
 */

namespace py app.thrift_gen.user

include "common.thrift"

/**
 * 用户状态枚举
 */
enum UserStatus {
    INACTIVE = 0,       // 未激活
    ACTIVE = 1,         // 已激活
    BANNED = 2,         // 已封禁
    DELETED = 3,        // 已删除
}

/**
 * 用户角色枚举
 */
enum UserRole {
    USER = 0,           // 普通用户
    ADMIN = 1,          // 管理员
    SUPERADMIN = 2,     // 超级管理员
}

// ============================================
// 数据传输对象 (DTO)
// ============================================

/**
 * 用户基础信息
 */
struct UserInfo {
    1: required i64 id,                     // 用户ID
    2: required string email,               // 邮箱
    3: required string username,            // 用户名
    4: optional string full_name,           // 全名
    5: required UserStatus status,          // 状态
    6: required UserRole role,              // 角色
    7: required i64 created_at,             // 创建时间戳
    8: required i64 updated_at,             // 更新时间戳
}

/**
 * 用户详细信息（包含敏感信息）
 */
struct UserDetail {
    1: required UserInfo base_info,         // 基础信息
    2: optional string phone,               // 手机号
    3: optional string avatar_url,          // 头像URL
    4: optional i64 last_login_at,          // 最后登录时间
    5: optional string last_login_ip,       // 最后登录IP
}

// ============================================
// 请求/响应结构
// ============================================

/**
 * 用户注册请求
 */
struct RegisterRequest {
    1: required string email,               // 邮箱
    2: required string username,            // 用户名 (3-50字符，字母数字)
    3: required string password,            // 密码 (8-100字符，需包含大小写和数字)
    4: optional string full_name,           // 全名
}

/**
 * 用户注册响应
 */
struct RegisterResponse {
    1: required common.BaseResponse base,   // 基础响应
    2: optional UserInfo user,              // 用户信息
}

/**
 * 用户登录请求
 */
struct LoginRequest {
    1: required string email,               // 邮箱
    2: required string password,            // 密码
    3: optional string device_id,           // 设备ID
    4: optional string device_type,         // 设备类型
}

/**
 * 登录令牌信息
 */
struct TokenInfo {
    1: required string access_token,        // 访问令牌
    2: required string refresh_token,       // 刷新令牌
    3: required string token_type,          // 令牌类型 (bearer)
    4: required i32 expires_in,             // 过期时间（秒）
}

/**
 * 用户登录响应
 */
struct LoginResponse {
    1: required common.BaseResponse base,   // 基础响应
    2: optional TokenInfo token,            // 令牌信息
    3: optional UserInfo user,              // 用户信息
}

/**
 * 刷新令牌请求
 */
struct RefreshTokenRequest {
    1: required string refresh_token,       // 刷新令牌
}

/**
 * 刷新令牌响应
 */
struct RefreshTokenResponse {
    1: required common.BaseResponse base,   // 基础响应
    2: optional TokenInfo token,            // 新令牌信息
}

/**
 * 获取用户请求
 */
struct GetUserRequest {
    1: required i64 user_id,                // 用户ID
}

/**
 * 获取用户响应
 */
struct GetUserResponse {
    1: required common.BaseResponse base,   // 基础响应
    2: optional UserDetail user,            // 用户详情
}

/**
 * 获取用户列表请求
 */
struct ListUsersRequest {
    1: required common.PaginationRequest pagination, // 分页参数
    2: optional UserStatus status,                   // 状态过滤
    3: optional UserRole role,                       // 角色过滤
    4: optional string search,                       // 搜索关键词
}

/**
 * 获取用户列表响应
 */
struct ListUsersResponse {
    1: required common.BaseResponse base,            // 基础响应
    2: optional list<UserInfo> users,                // 用户列表
    3: optional common.PaginationInfo pagination,    // 分页信息
}

/**
 * 更新用户请求
 */
struct UpdateUserRequest {
    1: required i64 user_id,                // 用户ID
    2: optional string email,               // 新邮箱
    3: optional string username,            // 新用户名
    4: optional string full_name,           // 新全名
    5: optional string phone,               // 新手机号
    6: optional string avatar_url,          // 新头像URL
}

/**
 * 更新用户响应
 */
struct UpdateUserResponse {
    1: required common.BaseResponse base,   // 基础响应
    2: optional UserInfo user,              // 更新后的用户信息
}

/**
 * 修改密码请求
 */
struct ChangePasswordRequest {
    1: required string old_password,        // 旧密码
    2: required string new_password,        // 新密码
}

/**
 * 修改密码响应
 */
struct ChangePasswordResponse {
    1: required common.BaseResponse base,   // 基础响应
}

/**
 * 删除用户请求
 */
struct DeleteUserRequest {
    1: required i64 user_id,                // 用户ID
    2: optional bool hard_delete,           // 是否硬删除
}

/**
 * 删除用户响应
 */
struct DeleteUserResponse {
    1: required common.BaseResponse base,   // 基础响应
}

// ============================================
// 服务接口定义
// ============================================

/**
 * 用户服务接口
 */
service UserService {
    /**
     * 用户注册
     */
    RegisterResponse Register(1: RegisterRequest request),
    
    /**
     * 用户登录
     */
    LoginResponse Login(1: LoginRequest request),
    
    /**
     * 刷新访问令牌
     */
    RefreshTokenResponse RefreshToken(1: RefreshTokenRequest request),
    
    /**
     * 获取用户信息
     */
    GetUserResponse GetUser(1: GetUserRequest request),
    
    /**
     * 获取用户列表
     */
    ListUsersResponse ListUsers(1: ListUsersRequest request),
    
    /**
     * 更新用户信息
     */
    UpdateUserResponse UpdateUser(1: UpdateUserRequest request),
    
    /**
     * 修改密码
     */
    ChangePasswordResponse ChangePassword(1: ChangePasswordRequest request),
    
    /**
     * 删除用户
     */
    DeleteUserResponse DeleteUser(1: DeleteUserRequest request),
}
