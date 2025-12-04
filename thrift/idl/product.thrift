/**
 * Product Service Thrift IDL
 * 产品服务 Thrift 接口定义
 */

namespace py product_service
namespace java com.example.product

/**
 * 产品信息
 */
struct ProductInfo {
    1: required i32 id,
    2: required string name,
    3: optional string description,
    4: required double price,
    5: required i32 stock,
    6: optional string category,
}

/**
 * 创建产品请求
 */
struct CreateProductRequest {
    1: required string name,
    2: optional string description,
    3: required double price,
    4: optional i32 stock = 0,
    5: optional string category,
}

/**
 * 产品列表响应
 */
struct ProductListResponse {
    1: required list<ProductInfo> products,
    2: required i32 total,
}

/**
 * 价格区间查询请求
 */
struct PriceRangeRequest {
    1: required double min_price,
    2: required double max_price,
    3: optional i32 skip = 0,
    4: optional i32 limit = 100,
}

/**
 * 库存更新请求
 */
struct StockUpdateRequest {
    1: required i32 product_id,
    2: required i32 quantity,
}

/**
 * 产品统计信息
 */
struct ProductStatistics {
    1: required string category,
    2: required i32 count,
    3: required double avg_price,
    4: required i32 total_stock,
}

/**
 * 通用响应
 */
struct Response {
    1: required i32 code,
    2: required string message,
}

/**
 * 产品服务异常
 */
exception ProductServiceException {
    1: required i32 code,
    2: required string message,
}

/**
 * 产品服务接口
 */
service ProductService {
    /**
     * 创建产品
     */
    ProductInfo createProduct(1: CreateProductRequest request) throws (1: ProductServiceException error),
    
    /**
     * 获取产品信息
     */
    ProductInfo getProduct(1: i32 product_id) throws (1: ProductServiceException error),
    
    /**
     * 获取产品列表
     */
    ProductListResponse listProducts(1: i32 skip, 2: i32 limit, 3: string category) throws (1: ProductServiceException error),
    
    /**
     * 更新产品
     */
    ProductInfo updateProduct(1: i32 product_id, 2: map<string, string> updates) throws (1: ProductServiceException error),
    
    /**
     * 删除产品
     */
    Response deleteProduct(1: i32 product_id) throws (1: ProductServiceException error),
    
    /**
     * 价格区间查询
     */
    ProductListResponse queryByPriceRange(1: PriceRangeRequest request) throws (1: ProductServiceException error),
    
    /**
     * 更新库存
     */
    ProductInfo updateStock(1: StockUpdateRequest request) throws (1: ProductServiceException error),
    
    /**
     * 获取分类统计
     */
    list<ProductStatistics> getStatistics() throws (1: ProductServiceException error),
}
