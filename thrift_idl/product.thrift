/**
 * Product Service Thrift Definition
 * 产品服务 Thrift 定义
 */

namespace py product_service

include "common.thrift"

/**
 * 产品信息结构
 */
struct ProductInfo {
    1: required i32 id,
    2: required string name,
    3: optional string description,
    4: required double price,
    5: required i32 stock,
    6: optional string category,
    7: optional i32 owner_id,
    8: optional string created_at,
    9: optional string updated_at
}

/**
 * 创建产品请求
 */
struct CreateProductRequest {
    1: required string name,
    2: optional string description,
    3: required double price,
    4: required i32 stock = 0,
    5: optional string category,
    6: optional i32 owner_id
}

/**
 * 更新产品请求
 */
struct UpdateProductRequest {
    1: optional string name,
    2: optional string description,
    3: optional double price,
    4: optional i32 stock,
    5: optional string category
}

/**
 * 产品列表响应
 */
struct ProductListResponse {
    1: required i32 total,
    2: required list<ProductInfo> items
}

/**
 * 分类统计结构
 */
struct CategoryStatistics {
    1: required string category,
    2: required i32 count,
    3: required double avg_price,
    4: required i32 total_stock
}

/**
 * 产品服务接口
 */
service ProductService {
    /**
     * 创建产品
     */
    ProductInfo createProduct(1: CreateProductRequest request) throws (1: common.ServiceException ex),
    
    /**
     * 获取产品详情
     */
    ProductInfo getProduct(1: i32 product_id) throws (1: common.ServiceException ex),
    
    /**
     * 获取产品列表
     */
    ProductListResponse listProducts(1: common.PaginationParams params) throws (1: common.ServiceException ex),
    
    /**
     * 更新产品
     */
    ProductInfo updateProduct(1: i32 product_id, 2: UpdateProductRequest request) throws (1: common.ServiceException ex),
    
    /**
     * 删除产品
     */
    bool deleteProduct(1: i32 product_id) throws (1: common.ServiceException ex),
    
    /**
     * 根据分类获取产品
     */
    ProductListResponse getProductsByCategory(1: string category, 2: common.PaginationParams params) throws (1: common.ServiceException ex),
    
    /**
     * 根据价格区间查询
     */
    ProductListResponse getProductsByPriceRange(1: double min_price, 2: double max_price, 3: common.PaginationParams params) throws (1: common.ServiceException ex),
    
    /**
     * 更新库存
     */
    ProductInfo updateStock(1: i32 product_id, 2: i32 quantity) throws (1: common.ServiceException ex),
    
    /**
     * 获取分类统计
     */
    list<CategoryStatistics> getCategoryStatistics() throws (1: common.ServiceException ex)
}
